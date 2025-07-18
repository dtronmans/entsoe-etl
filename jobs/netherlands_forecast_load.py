from datetime import datetime

from extract.extract import extract_forecast_load_n_days_prior
from transform.transform import transform_forecast_load_n_days_prior
from visualize.visualize_time_series import visualize_single_load_var


def netherlands_forecast_load(n_days=5):
    bidding_zone = "10YNL----------L"
    target_date = "2025-07-07"

    extracted_data = extract_forecast_load_n_days_prior(bidding_zone, target_date, n_days)
    transformed = [transform_forecast_load_n_days_prior(date_data[1], date_data[0]) for date_data in extracted_data]
    flattened = [item for day_data in transformed for item in day_data]

    for item in flattened:
        item['timestamp'] = datetime.fromisoformat(item['timestamp'])

    flattened.sort(key=lambda x: x['timestamp'])

    return flattened
