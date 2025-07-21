from extractors.load_forecast import LoadForecastExtractor
from jobs.netherlands_load import NetherlandsLoadJob
from loaders.visualize_loader import VisualizeLoader
from transformers.load_transformer import LoadTransformer
from utils.enums import LoadType

if __name__ == "__main__":
    job = NetherlandsLoadJob(
        extractor=LoadForecastExtractor(),
        transformer=LoadTransformer(),
        loader=VisualizeLoader()
    )

    job.run(
        bidding_zone="10YNL----------L",
        load_type=LoadType.FORECAST,
        target_date="2025-07-07",
        n_days=1
    )
