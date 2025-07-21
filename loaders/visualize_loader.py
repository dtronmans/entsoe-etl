from loaders.base import BaseLoader
import matplotlib.pyplot as plt


class VisualizeLoader(BaseLoader):
    def load(self, data: list[dict]):
        timestamps = [item['timestamp'] for item in data]
        load_values = [item['load_mw'] for item in data]

        plt.figure(figsize=(15, 5))
        plt.plot(timestamps, load_values, marker='o', linestyle='-')
        plt.xlabel("Time")
        plt.ylabel("Load (MW)")
        plt.title("Load Over Time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()
