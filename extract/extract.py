from zoneinfo import ZoneInfo

from datetime import datetime, timedelta, timezone

from api.api_caller import Caller


def extract_actual_load_five_days_prior(bidding_zone='10YFR-RTE------C', target_date=None):
    caller = Caller()

    print("Fetching from ENTSO-E API...")
    data_per_day = []

    if target_date is None:
        start_date = datetime.utcnow().date() - timedelta(days=2)
    else:
        start_date = datetime.strptime(target_date, "%Y-%m-%d").date()

    for i in range(5):
        date = start_date - timedelta(days=i)
        local_tz = ZoneInfo("Europe/Paris")

        local_start = datetime.combine(date, datetime.min.time(), tzinfo=local_tz)
        local_end = local_start + timedelta(days=1)

        start = local_start.astimezone(timezone.utc)
        end = local_end.astimezone(timezone.utc)

        day_data = caller.get_actual_load(start, end, bidding_zone)
        data_per_day.append((date, day_data))

    return data_per_day