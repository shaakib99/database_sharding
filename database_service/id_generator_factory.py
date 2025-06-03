from datetime import datetime, time
import hashlib
from base64 import b64encode

class IDGeneratorFactory:
    def __init__(self, max_server_id_length: int = 8, max_prefix_length: int = 6):
        self.number_of_slots = 2**max_server_id_length # we can have 256 servers, so 2^8 is enough
        self.max_server_id_length = max_server_id_length
        self.max_prefix_length = 2**max_prefix_length

    def _hash(self, s: str) -> int:
        return int(hashlib.md5(s.encode()).hexdigest(), 16)


    def _get_milliseconds_since_start_of_day(self) -> int:
        now = datetime.now()
        midnight = datetime.combine(now.date(), time.min)
        delta = now - midnight
        return int(delta.total_seconds() * 1000)

    def _prefix_to_int(self, s: str, ) -> int:
        return self._hash(s) % self.max_prefix_length

    def create(self, server_id: str, prefix: str | None = None) -> str:
        '''Generates a unique ID for the server based on the server ID and current datetime.
        The ID is a string that includes the server ID and the current millisecond timestamp.
        Characteristics:
        - First 8 bits are the server ID. 2^8 = 256 servers.
        - Next 6 bits are reserved for prefixes. 2^6 = 64 prefixes.
        - Next 27 bits are the current timestamp in milliseconds. 2^27 = 134217728 timestamps. enough for 24 hours.
        - Last 4 bits are reserved for concurrent use. 2^4 = 16 concurrent uses.
        '''
        server_id_bin = self._hash(server_id) % self.number_of_slots

        timestamp_ms = self._get_milliseconds_since_start_of_day()
        assert timestamp_ms < (1 << 27), "Timestamp exceeds 27 bits"

        prefix_bin = self._prefix_to_int(prefix) if prefix else 0

        unique_id = (server_id_bin << (6 + 27 + 4)) | (prefix_bin << (27 + 4)) | (timestamp_ms << 4) | 0
        

        # Convert integer to bytes (minimum necessary length)
        length = (unique_id.bit_length() + 7) // 8 or 1
        unique_id_bytes = unique_id.to_bytes(length, 'big')

        # Base64 encode and decode to ASCII string
        return b64encode(unique_id_bytes).decode('ascii')