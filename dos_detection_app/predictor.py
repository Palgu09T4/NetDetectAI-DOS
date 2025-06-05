import pandas as pd
import numpy as np
import joblib
import os

# Expected features
feature_columns = [
    'Flow Duration', 'Flow_Byts/s', 'Tot_Fwd_Pkts', 'Tot_Bwd_Pkts',
    'Fwd_Pkt_Len_Max', 'Bwd_Pkt_Len_Max', 'Fwd_IAT_Mean', 'Bwd_IAT_Mean',
    'SYN_Flag_Cnt', 'RST_Flag_Cnt', 'ACK_Flag_Cnt', 'Flow_Pkts/s'
]

reverse_label_mapping = {0: 'Normal', 1: 'DOS'}

# Lazy load functions
def get_model():
    return joblib.load('dos_rf_model.joblib')

def get_scaler():
    return joblib.load('scaler.joblib')


def predict_dos_from_csv(csv_path):
    model = get_model()
    scaler = get_scaler()

    df = pd.read_csv(csv_path)

    # Optional original info
    columns_to_keep = ['Time', 'Source', 'Destination', 'Protocol']
    extra_info_df = df[columns_to_keep].copy() if all(col in df.columns for col in columns_to_keep) else pd.DataFrame()

    # Drop unnecessary columns
    df = df.drop(columns=['Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info'], errors='ignore')

    # Check for missing columns
    missing_cols = set(feature_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required feature columns: {missing_cols}")

    df_features = df[feature_columns].apply(pd.to_numeric, errors='coerce')

    for col in feature_columns:
        mean_val = np.nanmean(df_features[col])
        df_features[col].fillna(mean_val if not np.isnan(mean_val) else 0, inplace=True)

    df_features.replace([np.inf, -np.inf], 0, inplace=True)

    # Scale + predict
    X_scaled = scaler.transform(df_features.values)
    preds = model.predict(X_scaled)
    probs = model.predict_proba(X_scaled)

    results = pd.DataFrame({
        'Row': df.index + 1,
        'Predicted_Label': [reverse_label_mapping[p] for p in preds],
        'Probability_Normal': probs[:, 0],
        'Probability_DOS': probs[:, 1]
    })

    if not extra_info_df.empty:
        extra_info_df = extra_info_df.reset_index(drop=True)
        final_df = pd.concat([extra_info_df, results], axis=1)
    else:
        final_df = results

    return final_df


def predict_dos_from_input(input_row):
    model = get_model()
    scaler = get_scaler()

    input_array = np.array(input_row).reshape(1, -1)
    input_scaled = scaler.transform(input_array)

    pred = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0]

    return {
        'Prediction': reverse_label_mapping[pred],
        'Probability_Normal': round(prob[0], 4),
        'Probability_DOS': round(prob[1], 4)
    }
