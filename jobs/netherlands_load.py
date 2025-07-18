from datetime import datetime

from extract.extract import extract_load_n_days_prior
from transform.transform import transform_load_vars


def netherlands_load(type_load, n_days=5):
    bidding_zone = "10YNL----------L"
    target_date = "2025-07-07"

    extracted_data = extract_load_n_days_prior(type_load, bidding_zone, target_date, n_days)
    transformed = [transform_load_vars(date_data[1], date_data[0]) for date_data in extracted_data]
    flattened = [item for day_data in transformed for item in day_data]

    for item in flattened:
        item['timestamp'] = datetime.fromisoformat(item['timestamp'])

    flattened.sort(key=lambda x: x['timestamp'])

    return flattened
