import random
from typing import Union, List, Optional
from tabulation_hashes.twisted_tabulation_hash import TwistedTabulationHash

class CuckooHashTable:
    def __init__(self, size: int = 11, max_displacements: int = 10):
        self.size = size
        self.max_displacements = max_displacements
        self.table = [None] * size
        self.hash1 = TwistedTabulationHash(seed=1)
        self.hash2 = TwistedTabulationHash(seed=2)

    def _position(self, key, which_hash):
        h = self.hash1 if which_hash == 1 else self.hash2
        return h.hash(key) % self.size

    def insert(self, key: Union[int, str, bytes]) -> bool:
        pos1 = self._position(key, 1)
        if self.table[pos1] is None:
            self.table[pos1] = key
            return True

        displaced = key
        for _ in range(self.max_displacements):
            pos1 = self._position(displaced, 1)
            displaced, self.table[pos1] = self.table[pos1], displaced

            pos2 = self._position(displaced, 2)
            if self.table[pos2] is None:
                self.table[pos2] = displaced
                return True

            displaced, self.table[pos2] = self.table[pos2], displaced

        # Rehashing needed
        return False

    def contains(self, key: Union[int, str, bytes]) -> bool:
        return (
            self.table[self._position(key, 1)] == key or
            self.table[self._position(key, 2)] == key
        )

    def __str__(self):
        return str(self.table)


if __name__ == "__main__":
    cuckoo = CuckooHashTable(size=11)
    keys = ["apple", "banana", "cherry", "date", "fig", "grape"]

    results = []
    for key in keys:
        success = cuckoo.insert(key)
        results.append((key, success))

    for key, inserted in results:
        estado = "Insertado" if inserted else "Falló"
        print(f"{key:>8}: {estado}")
