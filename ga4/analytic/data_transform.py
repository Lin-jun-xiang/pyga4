import base64
import json
from datetime import datetime, timedelta, timezone
from typing import Union, Iterable

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class Transformer:
    """Transform the data of GA4"""

    @staticmethod
    def decryptData(
        encoded_data: Union[str, Iterable],
        key = b'secret_key'
    ) -> Union[str, list]:
        """ Decrypt Data (string or json)
        """
        if isinstance(encoded_data, str):
            # 將 base64 編碼的數據解碼並進行解密
            encrypted_data = base64.b64decode(encoded_data)

            # 進行 Zero Padding
            key = key.ljust(16, b'\x00')

            # 創建 AES 解密器
            cipher = AES.new(key, AES.MODE_CBC, key)

            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

            try:
                json_data = decrypted_data.decode()
                data = json.loads(json_data)
            except (json.JSONDecodeError, UnicodeDecodeError):
                data = decrypted_data.decode()

            return data

        decrypted_list = []
        for item in encoded_data:
            decrypted_list.append(Transformer.decryptData(item, key))
        return decrypted_list

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
