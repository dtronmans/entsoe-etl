import matplotlib.pyplot as plt


def visualize_actual_load(flattened):
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
