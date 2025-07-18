from api.api_caller import Caller
from utils.date_utils import get_utc_day_ranges_before


def extract_actual_load_n_days_prior(bidding_zone='10YFR-RTE------C', target_date=None, n_days=5):
    caller = Caller()
    data_per_day = []

    day_ranges = get_utc_day_ranges_before(target_date, days=n_days)

    for date, start, end in day_ranges:
        day_data = caller.get_actual_load(start, end, bidding_zone)
        data_per_day.append((date, day_data))

    return data_per_day


def extract_forecast_load_n_days_prior(bidding_zone='10YFR-RTE------C', target_date=None, n_days=5):
    caller = Caller()
    data_per_day = []

    day_ranges = get_utc_day_ranges_before(target_date, days=n_days)

    for date, start, end in day_ranges:
        day_data = caller.get_forecast_load(start, end, bidding_zone)
        data_per_day.append((date, day_data))

    return data_per_day
