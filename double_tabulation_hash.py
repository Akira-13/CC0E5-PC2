import random
from typing import Union, List

class DoubleTabulationHash:
    def __init__(self, c: int = 4, r: int = 8, seed: int = None):
        """
        Double Tabulation Hashing:
        - c: Number of chunks (default: 4)
        - r: Bits per chunk (default: 8 → 1 byte)
        - seed: Seed for reproducibility
        """
        self.c = c
        self.r = r
        self.mask = (1 << r) - 1
        self.table_size = 1 << r

        random.seed(seed)
        # First layer: produces intermediate representation
        self.tables1 = [
            [random.getrandbits(r) for _ in range(self.table_size)]
            for _ in range(c)
        ]
        # Second layer: final hash from intermediate representation
        self.tables2 = [
            [random.getrandbits(32) for _ in range(self.table_size)]
            for _ in range(c)
        ]

    def _to_int(self, key: Union[int, bytes, str]) -> int:
        """Converts key to integer representation."""
        if isinstance(key, str):
            key = key.encode()
        if isinstance(key, bytes):
            key = int.from_bytes(key, byteorder='big')
        return key if isinstance(key, int) else int(key)

    def _chunked_key(self, key_int: int) -> List[int]:
        """Extracts 'c' chunks of 'r' bits from key_int."""
        return [(key_int >> (i * self.r)) & self.mask for i in range(self.c)]

    def _intermediate_chunks(self, chunks: List[int]) -> List[int]:
        """Uses tables1 to compute intermediate key from chunks."""
        return [self.tables1[i][chunk] for i, chunk in enumerate(chunks)]

    def _final_hash(self, intermediate: List[int]) -> int:
        """Uses tables2 to compute final hash from intermediate key."""
        h = 0
        for i, val in enumerate(intermediate):
            h ^= self.tables2[i][val]
        return h

    def hash(self, key: Union[int, bytes, str]) -> int:
        """Computes hash using double tabulation."""
        key_int = self._to_int(key)
        chunks = self._chunked_key(key_int)
        intermediate = self._intermediate_chunks(chunks)
        return self._final_hash(intermediate)

    def debug_hash(self, key: Union[int, bytes, str]) -> dict:
        """Returns full step-by-step hash computation for debugging."""
        key_int = self._to_int(key)
        chunks = self._chunked_key(key_int)
        intermediate = self._intermediate_chunks(chunks)
        final = self._final_hash(intermediate)
        return {
            "key_int": key_int,
            "chunks": chunks,
            "intermediate": intermediate,
            "final_hash": final
        }

if __name__ == "__main__":
    hasher_double = DoubleTabulationHash(seed=42)
    hash_double_int = hasher_double.hash(123456789)
    hash_double_str = hasher_double.hash("hello")

    print(f"  hash(123456789) = {hash_double_int}")
    print(f"  hash('hello')   = {hash_double_str}")