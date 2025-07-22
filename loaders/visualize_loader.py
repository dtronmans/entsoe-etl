from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from loaders.base import BaseLoader


class VisualizeLoader(BaseLoader):
    def load(self, data: list[dict]):
        # Convert ISO strings to datetime objects
        timestamps = [datetime.fromisoformat(item['timestamp']) for item in data]
        load_values = [item['load_mw'] for item in data]

        plt.figure(figsize=(15, 5))
        plt.plot(timestamps, load_values, marker='o', linestyle='-')

        plt.xlabel("Time")
        plt.ylabel("Load (MW)")
        plt.title("Actual Load Over Time")

        # Enable smart date formatting
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()
