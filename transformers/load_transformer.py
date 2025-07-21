import datetime
from xml.etree.ElementTree import Element

from isodate import parse_duration

from transformers.base import BaseTransformer


class LoadTransformer(BaseTransformer):
    def transform(self, root: Element, expected_date: datetime.date):
        load_values = []

        for time_series in root.findall('.//{*}TimeSeries'):
            for period in time_series.findall('{*}Period'):
                start_time = period.find('{*}timeInterval/{*}start').text
                resolution = period.find('{*}resolution').text
                points = period.findall('{*}Point')

                base_time = datetime.datetime.fromisoformat(start_time).replace(tzinfo=datetime.timezone.utc)

                for point in points:
                    position = int(point.find('{*}position').text)
                    quantity = float(point.find('{*}quantity').text)

                    duration = parse_duration(resolution)
                    utc_timestamp = base_time + duration * (position - 1)
                    local_timestamp = self._to_local_timestamp(utc_timestamp)

                    if local_timestamp.date() == expected_date:
                        load_values.append({
                            'timestamp': local_timestamp.isoformat(),
                            'load_mw': quantity
                        })

        return load_values
