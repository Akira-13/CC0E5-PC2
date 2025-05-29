import math
import random
import json
from tabulation_hashes.tabulation_hash import TabulationHash

# Serializa valores de forma determinista (JSON ordenado)
def consistent_stringify(value) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)

class BloomFilter:
    """
    Implementación de un Bloom filter con FNV-1 y MurmurHash3 para hashing múltiple.
    """
    def __init__(self, max_size: int, max_tolerance: float = 0.01, seed: int = None):
        # Validación de parámetros
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
        # Número de bits: m = -n ln p / (ln 2)^2
        self._num_bits = math.ceil(-max_size * math.log(tol) / (ln2**2))
        # Número de hashes: k = (m/n) ln 2  =>  k = -ln p / ln 2
        self._num_hashes = math.ceil(-math.log(tol) / ln2)

        # Prevención de filtros excesivamente grandes
        if self._num_bits > 1_000_000_000:
            raise MemoryError("Demasiada memoria requerida para el Bloom filter")

        # Tabulation hash functions generation
        self._tabhashes = [TabulationHash(seed=self._seed + i) for i in range(self._num_hashes)]

        num_bytes = math.ceil(self._num_bits / 8)
        self._bits = bytearray(num_bytes)  # Array de bytes para los bits
        self._size = 0                     # Conteo de inserciones únicas

    def _bit_coords(self, index: int):
        """Devuelve el índice de byte y el desplazamiento de bit para un índice global."""
        byte_idx = index // 8
        bit_idx = index % 8
        return byte_idx, bit_idx

    def _read_bit(self, index: int) -> int:
        """Lee el valor de un bit (0 o 1)."""
        b, i = self._bit_coords(index)
        return (self._bits[b] >> i) & 1

    def _write_bit(self, index: int) -> bool:
        """Establece un bit a 1. Devuelve True si cambió de estado."""
        b, i = self._bit_coords(index)
        mask = 1 << i
        old = self._bits[b]
        self._bits[b] |= mask
        return old != self._bits[b]

    def _key_positions(self, key: str):
        """Genera las posiciones de bit para una clave usando hashing doble."""
        s = consistent_stringify(key)
        for h in self._tabhashes:
            yield h.hash(s) % self._num_bits

    def add(self, value) -> "BloomFilter":
        """Añade un valor al filtro. Incrementa _size si algún bit cambió."""
        key = consistent_stringify(value)
        flipped = False
        for pos in self._key_positions(key):
            if self._write_bit(pos):
                flipped = True
        if flipped:
            self._size += 1
        return self

    def contains(self, value) -> bool:
        """Comprueba si un valor podría estar en el filtro (puede haber falsos positivos)."""
        key = consistent_stringify(value)
        return all(self._read_bit(pos) for pos in self._key_positions(key))

    @property
    def size(self) -> int:
        """Número de valores únicos insertados (aproximado)."""
        return self._size

    def false_positive_probability(self) -> float:
        """Calcula la probabilidad teórica de falso positivo."""
        k, n, m = self._num_hashes, self._size, self._num_bits
        return (1 - math.exp(-k * n / m))**k

    def confidence(self) -> float:
        """Devuelve la confianza (1 - probabilidad de falso positivo)."""
        return 1 - self.false_positive_probability()

    @property
    def max_remaining_capacity(self) -> int:
        """Capacidad restante antes de alcanzar max_size."""
        return max(0, self._max_size - self._size)
