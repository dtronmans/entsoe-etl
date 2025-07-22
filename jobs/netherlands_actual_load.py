from jobs.job import ETLJob
from utils.date_utils import get_utc_day_ranges_before
from utils.enums import LoadType


class NetherlandsActualLoad(ETLJob):
    def run(self, bidding_zone, load_type, target_date, n_days=1):
        all_transformed = []

        day_ranges = get_utc_day_ranges_before(target_date, days=n_days)
        for date, start, end in day_ranges:
            root = self.extractor.extract(
                start=start,
                end=end,
                bidding_zone=bidding_zone,
                load_type=load_type
            )
            transformed = self.transformer.transform(root, expected_date=date)
            all_transformed.extend(transformed)

        self.loader.load(all_transformed)
