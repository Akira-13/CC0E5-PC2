import math
import random
import json
from tabulation_hashes.tabulation_hash import TabulationHash

# Serializes value in deterministic fashion
def consistent_stringify(value) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)

class BloomFilter:
    """
    Bloom Filter implementation using Tabulation Hashing

    Generates the ideal amount of tabulation hash functions with different tables given
    a max tolerance to false positives and the amount of data to be added.
    """
    def __init__(self, max_size: int, max_tolerance: float = 0.01, seed: int = None):
        if not isinstance(max_size, int) or max_size <= 0:
            raise TypeError(f"maxSize debe ser un entero positivo, recibido: {max_size}")
        try:
            tol = float(max_tolerance)
        except:
            raise TypeError(f"tolerance debe ser un número en (0,1), recibido: {max_tolerance}")
        if tol <= 0 or tol >= 1:
            raise TypeError(f"tolerance debe cumplir 0 < t < 1, recibido: {max_tolerance}")
        if seed is None:
            seed = random.getrandbits(32)  # Semilla aleatoria si no se provee
        if not isinstance(seed, int):
            raise TypeError(f"seed debe ser un entero, recibido: {seed}")

        self._max_size = max_size
        self._seed = seed

        ln2 = math.log(2)
        # Number of bits: m = -n ln p / (ln 2)^2
        self._num_bits = math.ceil(-max_size * math.log(tol) / (ln2**2))
        # Number of hashes: k = (m/n) ln 2  =>  k = -ln p / ln 2
        self._num_hashes = math.ceil(-math.log(tol) / ln2)

        # Prevent excessively large filters
        if self._num_bits > 1_000_000_000:
            raise MemoryError("Demasiada memoria requerida para el Bloom filter")

        # Tabulation hash functions generation
        self._tabhashes = [TabulationHash(seed=self._seed + i) for i in range(self._num_hashes)]

        num_bytes = math.ceil(self._num_bits / 8)
        self._bits = bytearray(num_bytes)
        self._size = 0

    # Helper functions
    def _bit_coords(self, index: int):
        """Return byte index and bit position in bit."""
        byte_idx = index // 8
        bit_idx = index % 8
        return byte_idx, bit_idx

    def _read_bit(self, index: int) -> int:
        """Read bit value."""
        b, i = self._bit_coords(index)
        return (self._bits[b] >> i) & 1

    def _write_bit(self, index: int) -> bool:
        """Set bit to 1. Return True if it's been changed."""
        b, i = self._bit_coords(index)
        mask = 1 << i
        old = self._bits[b]
        self._bits[b] |= mask
        return old != self._bits[b]

    def _key_positions(self, key: str):
        """Generate positions of bits to check in further methods."""
        s = consistent_stringify(key)
        for h in self._tabhashes:
            yield h.hash(s) % self._num_bits

    # Interface
    def add(self, value) -> "BloomFilter":
        """Add value to filter."""
        key = consistent_stringify(value)
        flipped = False
        for pos in self._key_positions(key):
            if self._write_bit(pos):
                flipped = True
        if flipped:
            self._size += 1
        return self

    def contains(self, value) -> bool:
        """Check if a value is in filter."""
        key = consistent_stringify(value)
        return all(self._read_bit(pos) for pos in self._key_positions(key))

    @property
    def size(self) -> int:
        """Return approximate number of unique elements inserted."""
        return self._size

    def false_positive_probability(self) -> float:
        """Return theoretical false positive proability."""
        k, n, m = self._num_hashes, self._size, self._num_bits
        return (1 - math.exp(-k * n / m))**k

    def confidence(self) -> float:
        """Return 1 - false_positive_probability."""
        return 1 - self.false_positive_probability()

    @property
    def max_remaining_capacity(self) -> int:
        """Remaining capacity max_size - size"""
        return max(0, self._max_size - self._size)
