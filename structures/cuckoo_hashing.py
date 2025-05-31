import random
from typing import Union, List, Optional
from tabulation_hashes.twisted_tabulation_hash import TwistedTabulationHash

class CuckooHashTable:
    def __init__(self, size: int = 11, max_displacements: int = 10):
        if not isinstance(size, int) or size <= 0:
            raise TypeError(f"size must be a positive integer")
        
        if not isinstance(max_displacements, int) or max_displacements <= 0:
            raise TypeError(f"max_displacements must be a positive integer")
        
        self.size = size
        self.max_displacements = max_displacements
        self.table1 = [None] * size
        self.table2 = [None] * size
        self.hash1 = TwistedTabulationHash(seed=1)
        self.hash2 = TwistedTabulationHash(seed=2)

    def _position(self, key, which_hash):
        h = self.hash1 if which_hash == 1 else self.hash2
        return h.hash(key) % self.size

    def insert(self, key: Union[int, str, bytes]) -> bool:
        use_first = True
        displaced = key
        for _ in range(self.max_displacements):
            if use_first:
                pos = self._position(displaced, 1)
                if self.table1[pos] is None:
                    self.table1[pos] = displaced
                    return True
                displaced, self.table1[pos] = self.table1[pos], displaced
            else:
                pos = self._position(displaced, 2)
                if self.table2[pos] is None:
                    self.table2[pos] = displaced
                    return True
                displaced, self.table2[pos] = self.table2[pos], displaced
            # Alternar tabla
            use_first = not use_first

        # Rehashing needed
        return False

    def contains(self, key: Union[int, str, bytes]) -> bool:
        return (
            self.table1[self._position(key, 1)] == key or
            self.table2[self._position(key, 2)] == key
        )

    def __str__(self):
        return (f"Tabla1: {self.table1}\n"
                f"Tabla2: {self.table2}")


if __name__ == "__main__":
    cuckoo = CuckooHashTable(size=11)
    keys = ["apple", "banana", "cherry", "date", "fig", "grape"]

    for key in keys:
        inserted = cuckoo.insert(key)
        estado = "Insertado" if inserted else "Falló"
        print(f"{key:>8}: {estado}")

    print("\nEstado final de las tablas:")
    print(cuckoo)