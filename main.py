from extract import extract_actual_load
from transform import transform_actual_load
import matplotlib.pyplot as plt
from datetime import datetime

if __name__ == "__main__":
    API_KEY = "e784f7b7-627a-4987-a536-b2dd5956f4e2"
    bidding_zone = "10YNL----------L"

    extracted_data = extract_actual_load(API_KEY, bidding_zone, target_date="2025-07-07")
    transformed = [transform_actual_load(date_data[1], date_data[0]) for date_data in extracted_data]
    flattened = [item for day_data in transformed for item in day_data]

    for item in flattened:
        item['timestamp'] = datetime.fromisoformat(item['timestamp'])

    flattened.sort(key=lambda x: x['timestamp'])

    print(flattened)

    timestamps = [item['timestamp'] for item in flattened]
    load_values = [item['load_mw'] for item in flattened]

    plt.figure(figsize=(15, 5))
    plt.plot(timestamps, load_values, marker='o', linestyle='-')
    plt.xlabel("Time")
    plt.ylabel("Load (MW)")
    plt.title("Actual Load Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

