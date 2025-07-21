from datetime import datetime

from extract.extract import extract_load_n_days_prior
from transform.transform import transform_load_vars
from utils.date_utils import get_utc_day_ranges_before


class NetherlandsLoadJob:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self, *, target_date, n_days=1, **extract_kwargs):
        all_transformed = []

        day_ranges = get_utc_day_ranges_before(target_date, days=n_days)
        for date, start, end in day_ranges:
            extract_kwargs.update({"start": start, "end": end, "expected_date": date})
            root = self.extractor.extract(**extract_kwargs)
            transformed = self.transformer.transform(root, expected_date=date)
            all_transformed.extend(transformed)

        self.loader.load(all_transformed)
