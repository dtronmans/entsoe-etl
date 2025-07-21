from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def align_lists(forecast_flattened, actual_flattened):
    """
    Aligns two time series lists of dictionaries by common timestamps.
    Removes any entries that don't have a matching timestamp in the other list.

    Args:
        forecast_flattened (list): List of dicts with 'timestamp' and 'load_mw' for forecast data.
        actual_flattened (list): List of dicts with 'timestamp' and 'load_mw' for actual data.

    Returns:
        tuple: (aligned_forecast_flattened, aligned_actual_flattened)
    """
    forecast_dict = {entry['timestamp']: entry for entry in forecast_flattened}
    actual_dict = {entry['timestamp']: entry for entry in actual_flattened}

    common_timestamps = sorted(set(forecast_dict.keys()) & set(actual_dict.keys()))

    aligned_forecast = [forecast_dict[ts] for ts in common_timestamps]
    aligned_actual = [actual_dict[ts] for ts in common_timestamps]

    return aligned_forecast, aligned_actual


def get_utc_day_ranges_before(target_date: str = None, days: int = 5, tz: str = "Europe/Paris"):
    if target_date is None:
        start_date = datetime.utcnow().date() - timedelta(days=2)
    else:
        start_date = datetime.strptime(target_date, "%Y-%m-%d").date()

    day_ranges = []
    local_tz = ZoneInfo(tz)

    for i in range(days):
        date = start_date - timedelta(days=i)
        local_start = datetime.combine(date, datetime.min.time(), tzinfo=local_tz)
        local_end = local_start + timedelta(days=1)

        start_utc = local_start.astimezone(timezone.utc)
        end_utc = local_end.astimezone(timezone.utc)

        day_ranges.append((date, start_utc, end_utc))

    return day_ranges


def format_entsoe_datetime(dt):
    return dt.strftime('%Y%m%d%H%M')
