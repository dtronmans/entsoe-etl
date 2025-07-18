import matplotlib.pyplot as plt


def visualize_single_load_var(flattened):
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


def visualize_double_load_var(actual_flattened, forecast_flattened):
    timestamps_actual = [item['timestamp'] for item in actual_flattened]
    load_values_actual = [item['load_mw'] for item in actual_flattened]

    timestamps_forecast = [item['timestamp'] for item in forecast_flattened]
    load_values_forecast = [item['load_mw'] for item in forecast_flattened]

    plt.figure(figsize=(15, 5))
    plt.plot(timestamps_actual, load_values_actual, marker='o', linestyle='-', color='blue', label='Actual Load')
    plt.plot(timestamps_forecast, load_values_forecast, marker='x', linestyle='--', color='green',
             label='Forecast Load')

    plt.xlabel("Time")
    plt.ylabel("Load (MW)")
    plt.title("Actual vs Forecast Load Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
