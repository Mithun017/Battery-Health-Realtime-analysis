import pandas as pd
import requests
import time
import json
import random
import psutil

# Configuration
SERVER_URL = 'http://127.0.0.1:5000/update_sensor'
INTERVAL = 2  # Seconds between updates

def get_real_battery_data():
    """Fetches real battery status using psutil."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                'percent': battery.percent,
                'power_plugged': battery.power_plugged,
                'secsleft': battery.secsleft
            }
    except Exception:
        pass
    return None

def format_time_left(secs):
    if secs == psutil.POWER_TIME_UNLIMITED:
        return "Charging"
    if secs == psutil.POWER_TIME_UNKNOWN:
        return "Calculating..."
    
    hours = secs // 3600
    mins = (secs % 3600) // 60
    return f"{hours}h {mins}m"

def simulate_iot_device():
    print("Starting Real-time IoT Battery Simulator...")
    print("Press Ctrl+C to stop.")

    cycle_count = 50
    
    try:
        while True:
            real_data = get_real_battery_data()
            
            if real_data:
                # Use real system data
                percent = real_data['percent']
                
                # Map percentage to voltage (approximate Li-ion curve)
                # 100% -> 4.2V, 0% -> 3.0V
                voltage = 3.0 + (percent / 100.0) * 1.2
                
                # Add some noise
                voltage += random.uniform(-0.02, 0.02)
                
                # Current depends on charging status
                if real_data['power_plugged']:
                    current = random.uniform(0.5, 1.5) # Charging
                    time_left_str = "Charging"
                else:
                    current = random.uniform(-2.0, -0.5) # Discharging
                    time_left_str = format_time_left(real_data['secsleft'])
                
                real_percent = percent
                
            else:
                # Fallback to random simulation if no battery detected
                voltage = random.uniform(3.2, 4.2)
                current = random.uniform(-1.5, -0.5)
                real_percent = int((voltage - 3.0) / 1.2 * 100)
                time_left_str = "N/A (Simulated)"
            
            # Random temperature
            temperature = random.uniform(25.0, 35.0)
            
            # Slowly increase cycle count
            if random.random() < 0.01:
                cycle_count += 1

            payload = {
                'voltage': round(voltage, 3),
                'current': round(current, 3),
                'temperature': round(temperature, 1),
                'cycle': cycle_count,
                'real_percent': real_percent,
                'real_time_left': time_left_str
            }
            
            try:
                response = requests.post(SERVER_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    print(f"Sent: {payload['real_percent']}% | {payload['voltage']}V | {payload['real_time_left']} -> SoH: {data.get('soh', 'N/A'):.2f}%")
                else:
                    print(f"Failed to send data. Status: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print("Connection refused. Is the server running?")
            
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    simulate_iot_device()
