from extractors.load_forecast import LoadForecastExtractor
from utils.date_utils import get_utc_day_ranges_before


def extract_multiple_days(
    load_type, bidding_zone="10YFR-RTE------C", target_date=None, n_days=5
):
    extractor = LoadForecastExtractor()
    data_per_day = []

    day_ranges = get_utc_day_ranges_before(target_date, days=n_days)

    for date, start, end in day_ranges:
        root = extractor.extract(start, end, bidding_zone, load_type)
        data_per_day.append((date, root))  # (datetime.date, XML root)

    return data_per_day
