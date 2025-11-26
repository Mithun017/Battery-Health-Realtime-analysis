# IoT-Driven Smart Battery Failure Forecasting

A machine-learning based battery health prediction system that estimates the State of Health (SoH) of a Li-ion battery in real-time. It uses the NASA Battery Life Prediction dataset and includes a real-time hardware simulator.

## Features

-   **Machine Learning Model**: Random Forest Regressor trained on NASA's battery dataset.
-   **Real-time Simulation**: A Python script mimics an IoT device sending live voltage, current, and temperature data.
-   **Live Dashboard**: Web interface updates automatically every 5 seconds with live data.
-   **Health Prediction**: Instantly predicts if the battery is in "Good Condition", "Degradation Detected", or needs "Replacement".

## Project Structure

-   `data/`: Contains the dataset (`discharge.csv`).
-   `model/`: Training script (`train_model.py`) and saved model (`battery_model.pkl`).
-   `server/`: Flask backend (`app.py`) handling predictions and live data storage.
-   `static/`: Frontend (`index.html`, `style.css`, `script.js`).
-   `simulate_hardware.py`: Script to simulate real-time IoT sensor data.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Mithun017/Battery-Health-Realtime-analysis.git
    cd Battery-Health-Realtime-analysis
    ```

2.  **Install Dependencies**:
    ```bash
    pip install pandas numpy scikit-learn flask flask-cors joblib requests
    ```

## How to Run

### 1. Start the Backend Server
This runs the API and serves the web application.
```bash
python server/app.py
```
*Server runs at http://127.0.0.1:5000*

### 2. Start the Hardware Simulator
Open a **new terminal** and run this script to start sending live data.
```bash
python simulate_hardware.py
```

### 3. Open the Dashboard
Open `static/index.html` in your web browser. You will see the "Live IoT Monitor" updating automatically.

## Model Training (Optional)
If you want to retrain the model:
```bash
python model/train_model.py
```

## License
This project is open-source.
