# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv('training_data.csv')

feature_columns = [
    'Flow Duration', 'Flow_Byts/s', 'Tot_Fwd_Pkts', 'Tot_Bwd_Pkts', 
    'Fwd_Pkt_Len_Max', 'Bwd_Pkt_Len_Max', 'Fwd_IAT_Mean', 'Bwd_IAT_Mean',
    'SYN_Flag_Cnt', 'RST_Flag_Cnt', 'ACK_Flag_Cnt', 'Flow_Pkts/s'
]
label_column = 'Label'

# Clean dataframe
df = df.drop(columns=['Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info'], errors='ignore')
df[feature_columns] = df[feature_columns].apply(pd.to_numeric, errors='coerce')

label_mapping = {'Normal': 0, 'DOS': 1}
df[label_column] = df[label_column].map(label_mapping)

if df[label_column].isna().sum() > 0:
    raise ValueError("Unmapped labels detected in dataset")

X = df[feature_columns].values
y = df[label_column].values.astype(np.float32)

# Fix NaNs and infinite values
X[np.isnan(X)] = np.nanmean(X)
X[np.isinf(X)] = 0

# Scale features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train RandomForest with GridSearchCV for best params
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [None, 10],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'bootstrap': [True]
}

clf = RandomForestClassifier(random_state=42)
grid = GridSearchCV(clf, param_grid, cv=3, n_jobs=-1, scoring='accuracy')
grid.fit(X_train, y_train)

best_model = grid.best_estimator_
print("Best Params:", grid.best_params_)

# Test accuracy
y_pred = best_model.predict(X_test)
print("Test Accuracy:", accuracy_score(y_test, y_pred))

# Save model and scaler
joblib.dump(best_model, 'dos_rf_model.joblib')
joblib.dump(scaler, 'scaler.joblib')
print("Model and scaler saved!")
