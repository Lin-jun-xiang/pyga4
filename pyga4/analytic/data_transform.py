import base64
from datetime import datetime, timedelta, timezone
from typing import Union, Iterable


class Transformer:
    """Transform the data of GA4"""
    @staticmethod
    def timestamp_to_datetime(
        ga4_timestamp: Union[str, Iterable]
    ) -> Union[str, list]:
        if isinstance(ga4_timestamp, str):
            ga4_timestamp_seconds = int(ga4_timestamp) / 1e6

            # Create a datetime object in UTC timezone
            utc_datetime = datetime.fromtimestamp(ga4_timestamp_seconds, tz=timezone.utc)

            # Convert to Taiwan timezone
            taiwan_timezone = timezone(timedelta(hours=8))
            taiwan_datetime = utc_datetime.astimezone(taiwan_timezone)

            return taiwan_datetime

        timestamp_list = []
        for timestamp in ga4_timestamp:
            timestamp_list.append(Transformer.timestamp_to_datetime(timestamp))
        return timestamp_list
