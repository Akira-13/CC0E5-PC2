import pytest
from structures.cuckoo_hashing import CuckooHashTable

def test_create_valid_cuckoo_table():
    table = CuckooHashTable(size=11, max_displacements=5)
    assert isinstance(table, CuckooHashTable)

def test_invalid_size_type():
    with pytest.raises(TypeError, match="size must be a positive integer"):
        CuckooHashTable(size="million")

def test_invalid_size_value():
    with pytest.raises(TypeError, match="size must be a positive integer"):
        CuckooHashTable(size=-30)

def test_invalid_max_displacements_type():
    with pytest.raises(TypeError, match="max_displacements must be a positive integer"):
        CuckooHashTable(size=10, max_displacements="ten")

def test_invalid_max_displacements_value():
    with pytest.raises(TypeError, match="max_displacements must be a positive integer"):
        CuckooHashTable(size=10, max_displacements=-5)

def test_insert_and_contains():
    table = CuckooHashTable(size=11, max_displacements=10)
    keys = [15, 23, 37]

    for key in keys:
        inserted = table.insert(key)
        assert inserted, f"{key} should be inserted"
        assert table.contains(key), f"{key} should be found after insertion"

def test_insert_duplicate_key():
    table = CuckooHashTable(size=11)
    key = 42
    assert table.insert(key)
    assert table.insert(key), "inserting the same key again should not fail"
    assert table.contains(key)

def test_insertion_failure_due_to_collisions():
    table = CuckooHashTable(size=3, max_displacements=5)
    keys = [1, 2, 3, 4, 5, 6]

    results = [table.insert(k) for k in keys]
    assert any(not r for r in results), "at least one insertion should fail due to limited table size"

def test_key_not_present():
    table = CuckooHashTable(size=11)
    table.insert("hello")
    assert not table.contains("world"), "key 'world' was never inserted"

def test_table_str_representation():
    table = CuckooHashTable(size=5)
    table.insert("x")
    s = str(table)
    assert isinstance(s, str)
    assert "x" in s or "None" in s 

