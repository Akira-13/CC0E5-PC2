import math
import random
from tabulation_hashes.tabulation_hash import TabulationHash

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
            seed = random.getrandbits(32)
        if not isinstance(seed, int):
            raise TypeError(f"seed debe ser un entero, recibido: {seed}")

        self._max_size = max_size
        self._seed = seed

        ln2 = math.log(2)
        self._num_bits = math.ceil(-max_size * math.log(tol) / (ln2**2))
        self._num_hashes = math.ceil(-math.log(tol) / ln2)

        if self._num_bits > 1_000_000_000:
            raise MemoryError("Demasiada memoria requerida para el Bloom filter")

        self._tabhashes = [TabulationHash(seed=self._seed + i) for i in range(self._num_hashes)]
        self._bits = bytearray(math.ceil(self._num_bits / 8))
        self._size = 0

    # Helper methods
    def _bit_coords(self, index: int):
        byte_idx = index // 8
        bit_idx = index % 8
        return byte_idx, bit_idx

    def _read_bit(self, index: int) -> int:
        b, i = self._bit_coords(index)
        return (self._bits[b] >> i) & 1

    def _write_bit(self, index: int) -> bool:
        b, i = self._bit_coords(index)
        mask = 1 << i
        old = self._bits[b]
        self._bits[b] |= mask
        return old != self._bits[b]

    # Interface
    def _to_bytes(self, value) -> bytes:
        if isinstance(value, bytes):
            return value
        elif isinstance(value, str):
            return value.encode('utf-8')
        elif isinstance(value, int):
            return value.to_bytes(8, byteorder='big', signed=True)
        else:
            return repr(value).encode('utf-8')

    def _key_positions(self, value):
        b = self._to_bytes(value)
        for h in self._tabhashes:
            yield h.hash(b) % self._num_bits

    def add(self, value) -> "BloomFilter":
        flipped = False
        for pos in self._key_positions(value):
            if self._write_bit(pos):
                flipped = True
        if flipped:
            self._size += 1
        return self

    def contains(self, value) -> bool:
        return all(self._read_bit(pos) for pos in self._key_positions(value))

    @property
    def size(self) -> int:
        return self._size

    def false_positive_probability(self) -> float:
        k, n, m = self._num_hashes, self._size, self._num_bits
        return (1 - math.exp(-k * n / m))**k

    def confidence(self) -> float:
        return 1 - self.false_positive_probability()

    @property
    def max_remaining_capacity(self) -> int:
        return max(0, self._max_size - self._size)
