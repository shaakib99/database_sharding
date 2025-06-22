from datetime import datetime, timezone
import hashlib
from base64 import b64encode

class IDGeneratorService:
    def __init__(self, max_server_id_length: int = 8, max_prefix_length: int = 6):
        self.number_of_slots = 2 ** max_server_id_length  # 256 servers
        self.max_server_id_length = max_server_id_length
        self.max_prefix_length = 2 ** max_prefix_length   # 64 prefixes

    def _hash(self, s: str) -> int:
        return int(hashlib.md5(s.encode()).hexdigest(), 16)

    def _prefix_to_int(self, s: str) -> int:
        return self._hash(s) % self.max_prefix_length

    def _get_epoch_ms(self) -> int:
        """Returns milliseconds since Unix epoch (Jan 1, 1970 UTC)"""
        return int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    def generate(self, prefix: str | None = None) -> str:
        """
        ID Structure (52 bits total):
        - 6 bits: prefix ID
        - 42 bits: epoch time in ms
        - 4 bits: reserved for concurrency
        - Id will 12 characters long
        """
        prefix_bin = self._prefix_to_int(prefix) if prefix else 0
        epoch_ms = self._get_epoch_ms()
        assert epoch_ms < (1 << 42), "Epoch timestamp exceeds 42-bit limit"

        unique_id = (
            (prefix_bin << (42 + 4)) |
            (epoch_ms << 4) |
            0  # Placeholder for concurrency bits
        )

        byte_len = (unique_id.bit_length() + 7) // 8 or 1
        unique_id_bytes = unique_id.to_bytes(byte_len, 'big')
        return b64encode(unique_id_bytes).decode('ascii')
