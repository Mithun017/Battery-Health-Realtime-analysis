import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os

def load_and_process_data(filepath):
    """
    Loads dataset, calculates SoH, and selects features.
    """
    print(f"Loading data from {filepath}...")
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None, None, None

    # Check for expected columns
    expected_cols = ['voltage', 'current', 'temperature', 'cycle', 'capacity']
    # The dataset from fmardero/battery_aging might have different column names.
    # Let's inspect the first few lines if we could, but here we'll assume standard names or map them.
    # Based on common versions of this dataset:
    # It might be 'voltage_measured', 'current_measured', 'temperature_measured', 'cycle', 'capacity'
    
    # Let's standardize column names
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Mapping common variations to standard names
    rename_map = {
        'voltage_measured': 'voltage',
        'current_measured': 'current',
        'temperature_measured': 'temperature',
        'cycle_index': 'cycle',
        'id_cycle': 'cycle'
    }
    df.rename(columns=rename_map, inplace=True)

    # Ensure we have the required columns
    required_cols = ['voltage', 'current', 'temperature', 'cycle', 'capacity']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        print(f"Error: Missing columns: {missing_cols}")
        print(f"Available columns: {df.columns.tolist()}")
        return None, None, None

    # Calculate State of Health (SoH)
    # SoH = (Current Capacity / Initial Capacity) * 100
    # We assume the max capacity observed in the first few cycles is the initial capacity
    # Or simply the max capacity in the dataset if it starts fresh.
    initial_capacity = df['capacity'].max()
    df['soh'] = (df['capacity'] / initial_capacity) * 100
    
    print(f"Initial Capacity determined as: {initial_capacity}")

    # Select features and target
    features = ['voltage', 'current', 'temperature', 'cycle']
    target = 'soh'

    X = df[features]
    y = df[target]

    return X, y, initial_capacity

def train_model(X, y):
    """
    Trains a Random Forest Regressor.
    """
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"Model Performance:")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")

    return model

def main():
    data_path = 'data/discharge.csv'
    model_path = 'model/battery_model.pkl'

    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('model'):
        os.makedirs('model')

    X, y, _ = load_and_process_data(data_path)
    
    if X is not None and y is not None:
        model = train_model(X, y)
        
        print(f"Saving model to {model_path}...")
        joblib.dump(model, model_path)
        print("Done.")
    else:
        print("Failed to process data.")

if __name__ == "__main__":
    main()
