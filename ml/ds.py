import pandas as pd
import random

def generate_vehicle_data(num_samples=1000):
    data = []
    
    for _ in range(num_samples):
        engine_temp = round(random.uniform(30, 50), 2)  # Engine temperature in °C
        runtime = random.randint(100, 500)  # Engine runtime in hours
        throttle = random.randint(50, 100)  # Throttle percentage
        rpm = random.randint(100, 200)  # Engine RPM
        
        # Determine maintenance status
        if runtime >= 300:
            maintenance_status = 1  # Needs maintenance
        elif engine_temp >= 37 or throttle >= 80 or rpm >= 120:
            maintenance_status = 2  # Abnormal conditions
        else:
            maintenance_status = 0  # Normal
        
        data.append([engine_temp, runtime, throttle, rpm, maintenance_status])
    
    return pd.DataFrame(data, columns=["Engine_Temperature", "Runtime", "Throttle", "RPM", "Maintenance_Status"])

# Generate dataset
df = generate_vehicle_data(1000)

# Save to CSV
df.to_csv("vehicle_monitoring_data.csv", index=False)

print("Dataset generated and saved as vehicle_monitoring_data.csv")
