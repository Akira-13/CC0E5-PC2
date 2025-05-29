from structures.cuckoo_hashing import CuckooHashTable

def test_insert_and_contains():
    table = CuckooHashTable(size=11, max_displacements=10)
    keys = [15, 23, 37]

    for key in keys:
        assert table.insert(key), f"La clave {key} debería insertarse correctamente"
        assert table.contains(key), f"La clave {key} debería encontrarse"

def test_duplicate_insertion():
    table = CuckooHashTable(size=11)
    key = 42
    assert table.insert(key)
    assert table.insert(key)  
    assert table.contains(key)

def test_fail_insertion():
    small_table = CuckooHashTable(size=3, max_displacements=5)
    keys = [1, 2, 3, 4, 5, 6]
    inserted = [small_table.insert(k) for k in keys]
    assert False in inserted, "Debería fallar al menos una inserción por tabla pequeña"

def test_not_contains():
    table = CuckooHashTable(size=11)
    table.insert(10)
    assert not table.contains(99), "La clave 99 no debería estar en la tabla"
