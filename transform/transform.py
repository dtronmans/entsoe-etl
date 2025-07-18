from zoneinfo import ZoneInfo  # Python 3.9+
from datetime import datetime, timedelta, timezone
from isodate import parse_duration


def transform_load_vars(root, expected_date, tz_str='Europe/Paris'):
    load_values = []
    local_tz = ZoneInfo(tz_str)

    for time_series in root.findall('.//{*}TimeSeries'):
        for period in time_series.findall('{*}Period'):
            start_time = period.find('{*}timeInterval/{*}start').text
            resolution = period.find('{*}resolution').text
            points = period.findall('{*}Point')

            # Parse start_time as UTC-aware datetime
            base_time = datetime.fromisoformat(start_time).replace(tzinfo=timezone.utc)

            for point in points:
                position = int(point.find('{*}position').text)
                quantity = float(point.find('{*}quantity').text)

                # Add time delta and convert to local time
                duration = parse_duration(resolution)  # this makes it sensitive to 1 hour vs. 15 minutes
                utc_timestamp = base_time + duration * (position - 1)
                local_timestamp = utc_timestamp.astimezone(local_tz)

                if local_timestamp.date() == expected_date:
                    load_values.append({
                        'timestamp': local_timestamp.isoformat(),
                        'load_mw': quantity
                    })

    return load_values
