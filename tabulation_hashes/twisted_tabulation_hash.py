import random
from typing import Union, List

class TwistedTabulationHash:
    def __init__(self, c: int = 4, r: int = 8, seed: int = None):
        """
        Twisted Tabulation Hashing:
        - c: number of chunks (default: 4)
        - r: bits per chunk (default: 8)
        - seed: random seed for reproducibility
        """
        self.c = c
        self.r = r
        self.mask = (1 << r) - 1
        self.table_size = 1 << r

        random.seed(seed)
        # Create c tables of 2^r entries with 32-bit values
        self.tables = [
            [random.getrandbits(32) for _ in range(self.table_size)]
            for _ in range(c)
        ]
        # An additional "twister" table for the final XOR (used for dependency-breaking)
        self.twister = [random.getrandbits(32) for _ in range(self.table_size)]

    def _to_int(self, key: Union[int, bytes, str]) -> int:
        if isinstance(key, str):
            key = key.encode()
        if isinstance(key, bytes):
            key = int.from_bytes(key, byteorder='big')
        return key if isinstance(key, int) else int(key)

    def _chunked_key(self, key_int: int) -> List[int]:
        return [(key_int >> (i * self.r)) & self.mask for i in range(self.c)]

    def hash(self, key: Union[int, bytes, str]) -> int:
        key_int = self._to_int(key)
        chunks = self._chunked_key(key_int)

        # Base: XOR of all table lookups
        h = 0
        for i in range(self.c):
            h ^= self.tables[i][chunks[i]]

        # Twist: XOR with a special entry based on XOR of all chunks
        twist_index = 0
        for chunk in chunks:
            twist_index ^= chunk  # XOR all chunk values
        h ^= self.twister[twist_index]

        return h

# Ejemplo simple
if __name__ == "__main__":
    hasher_twisted = TwistedTabulationHash(seed=42)
    print("Twisted hash of 123456789:", hasher_twisted.hash(123456789))
    print("Twisted hash of 'hello':", hasher_twisted.hash("hello"))
