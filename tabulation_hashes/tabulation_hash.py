import random
from typing import Union

class TabulationHash:
    def __init__(self, c: int = 4, r: int = 8, seed: int = None):
        """
        Tabulation hashing with:
        - c: Number of chunks (default: 4)
        - r: Bits per chunk (default: 8 → 1 byte)
        - seed: For testing reproducibility (default: None)
        """
        self.c = c
        self.r = r
        self.mask = (1 << r) - 1  # Bitmask for extracting r bits
        self.table_size = 1 << r  # 2^r entries per table
        
        random.seed(seed)
        # Initialize table
        # Create 32-bit random numbers for 2^r entries
        # One table per chunk: c tables in total
        self.tables = [
            [random.getrandbits(32) for _ in range(self.table_size)]
            for _ in range(c)
        ]

    def hash(self, key: Union[int, bytes, str]) -> int:
        """Hash an integer, bytes, or string."""
        if isinstance(key, str):
            key = key.encode()  # string -> bytes
        if isinstance(key, bytes):
            key = int.from_bytes(key, byteorder='big') # bytes -> int
        
        h = 0
        for i in range(self.c):
            # Extract the i-th r-bit chunk
            # 1. Shift to the right the key up to the i-th chunk
            # 2. Apply mask to isolate r-sized chunk
            chunk = (key >> (i * self.r)) & self.mask
            # 3. XOR the value in the table indexed by the chunk with hash so far
            h ^= self.tables[i][chunk]
        return h

if __name__ == "__main__":
    hasher = TabulationHash(seed=42)
    print(hasher.hash(123456789))  # Example: 1098894519
    print(hasher.hash("hello"))    # Example: 3381460645
