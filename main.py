from datetime import date

from extractors.load_forecast import LoadForecastExtractor
from jobs.job import ETLJob
from jobs.netherlands_load import NetherlandsLoadJob
from transformers.load_transformer import LoadTransformer
from utils.enums import LoadType
from utils.date_utils import align_lists
from visualize.visualize_time_series import visualize_double_load_var


class PrintLoader:
    def load(self, data):
        print(f"\n--- Loaded {len(data)} records ---")
        for item in data[:5]:  # just print first 5
            print(item)
        if len(data) > 5:
            print("... (truncated)\n")


if __name__ == "__main__":
    job = NetherlandsLoadJob(
        extractor=LoadForecastExtractor(),
        transformer=LoadTransformer(),
        loader=PrintLoader()
    )

    job.run(
        bidding_zone="10YNL----------L",
        load_type=LoadType.FORECAST,
        target_date=date(2025, 7, 7),
        n_days=3
    )
