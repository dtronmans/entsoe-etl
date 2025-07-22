from zoneinfo import ZoneInfo


class BaseTransformer:
    def __init__(self, tz_str="Europe/Paris"):
        self.local_tz = ZoneInfo(tz_str)

    def _to_local_timestamp(self, utc_dt):
        return utc_dt.astimezone(self.local_tz)
