from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


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
