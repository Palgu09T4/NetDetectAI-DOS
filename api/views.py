from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .serializers import ManualInputSerializer
import joblib
import numpy as np
import pandas as pd
from django.core.files.storage import default_storage
import os
from django.views.decorators.csrf import csrf_exempt

# Load your trained model
model = joblib.load('dos_rf_model.joblib')  # Adjust path if needed
scaler = joblib.load('scaler.joblib')
reverse_label_mapping = {0: "Normal", 1: "DoS Attack"}

@api_view(['POST'])
def predict_manual(request):
    rename_map = {
        'Flow Duration': 'Flow_Duration',
        'Flow_Byts/s': 'Flow_Byts_s',
        'Flow_Pkts/s': 'Flow_Pkts_s'
        # Add others if necessary
    }

    data = request.data.copy()  # make mutable copy if necessary

    for old_key, new_key in rename_map.items():
        if old_key in data:
            data[new_key] = data.pop(old_key)

    serializer = ManualInputSerializer(data=data)
    if serializer.is_valid():
        features = list(serializer.validated_data.values())
        prediction = model.predict([features])[0]
        result = "DoS Attack" if prediction == 1 else "Normal"
        return Response({"prediction": result})
    else:
        print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@parser_classes([MultiPartParser])
def predict_csv(request):
    if 'file' not in request.FILES:
        return Response({"error": "CSV file not provided."}, status=status.HTTP_400_BAD_REQUEST)

    csv_file = request.FILES['file']
    file_path = default_storage.save('tmp/' + csv_file.name, csv_file)

    try:
        df = pd.read_csv(default_storage.path(file_path))

        df.columns = df.columns.str.strip()
        df.rename(columns={
            'Flow Duration': 'Flow_Duration',
            'Flow_Byts/s': 'Flow_Byts_s',
            'Flow_Pkts/s': 'Flow_Pkts_s'
        }, inplace=True)

        df = df.drop(columns=['Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info'], errors='ignore')

        feature_columns = [
            'Flow_Duration', 'Flow_Byts_s', 'Tot_Fwd_Pkts', 'Tot_Bwd_Pkts',
            'Fwd_Pkt_Len_Max', 'Bwd_Pkt_Len_Max', 'Fwd_IAT_Mean', 'Bwd_IAT_Mean',
            'SYN_Flag_Cnt', 'RST_Flag_Cnt', 'ACK_Flag_Cnt', 'Flow_Pkts_s'
        ]

        missing_cols = set(feature_columns) - set(df.columns)
        if missing_cols:
            return Response({"error": f"Missing columns in input CSV: {missing_cols}"}, status=status.HTTP_400_BAD_REQUEST)

        df_features = df[feature_columns].apply(
            lambda col: pd.to_numeric(col.astype(str).str.replace(',', ''), errors='coerce')
        )

        for col in feature_columns:
            mean_val = np.nanmean(df_features[col])
            if np.isnan(mean_val):
                mean_val = 0
            df_features[col].fillna(mean_val, inplace=True)

        df_features.replace([np.inf, -np.inf], 0, inplace=True)

        X_scaled = scaler.transform(df_features.values)
        preds = model.predict(X_scaled)
        probs = model.predict_proba(X_scaled)

        results = pd.DataFrame({
            'Row': df.index + 1,
            'Predicted_Label': [reverse_label_mapping[p] for p in preds],
            'Probability_Normal': probs[:, 0],
            'Probability_DOS': probs[:, 1]
        })

        # Save predictions to CSV (excluding summary)
        output_dir = 'results'
        os.makedirs(default_storage.path(output_dir), exist_ok=True)
        output_filename = 'dos_predictions.csv'
        output_path = os.path.join(output_dir, output_filename)
        with default_storage.open(output_path, 'w') as f:
            results.to_csv(f, index=False)

        # Generate summary for chart
        summary = {
            "Normal": int((results['Predicted_Label'] == 'Normal').sum()),
            "DoS Attack": int((results['Predicted_Label'] == 'DoS Attack').sum())
        }

        download_link = default_storage.url(output_path)

        return Response({
            "download_link": download_link,
            "summary": summary
        })

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)

