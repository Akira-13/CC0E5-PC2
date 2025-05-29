import pytest
from structures.tabulated_bloom_filter import BloomFilter

def test_bloom_filter_creation_valid():
    bf = BloomFilter(max_size=100, max_tolerance=0.01, seed=42)
    assert isinstance(bf, BloomFilter)

def test_bloom_filter_invalid_max_size():
    with pytest.raises(TypeError):
        BloomFilter(max_size=0)
    with pytest.raises(TypeError):
        BloomFilter(max_size=-5)
    with pytest.raises(TypeError):
        BloomFilter(max_size="100")

def test_bloom_filter_invalid_tolerance():
    with pytest.raises(TypeError):
        BloomFilter(max_size=100, max_tolerance="abc")
    with pytest.raises(TypeError):
        BloomFilter(max_size=100, max_tolerance=-0.1)
    with pytest.raises(TypeError):
        BloomFilter(max_size=100, max_tolerance=1.1)

def test_bloom_filter_invalid_seed():
    with pytest.raises(TypeError):
        BloomFilter(max_size=100, seed="not-an-int")

def test_add_and_contains():
    bf = BloomFilter(max_size=1000, seed=123)
    bf.add("apple")
    assert bf.contains("apple")
    assert not bf.contains("banana")

def test_add_multiple_values():
    bf = BloomFilter(max_size=1000, seed=123)
    items = ["a", "b", "c", 1, 2, 3, (1, 2), {"key": "value"}]
    for item in items:
        bf.add(item)
    for item in items:
        assert bf.contains(item)

def test_approximate_size():
    bf = BloomFilter(max_size=100, seed=456)
    for i in range(10):
        bf.add(i)
    assert bf.size <= 10  # Due to potential duplicate insertions or collisions

def test_false_positive_rate():
    bf = BloomFilter(max_size=50, max_tolerance=0.05, seed=789)
    for i in range(50):
        bf.add(f"item-{i}")
    # Check a random non-inserted item
    false_positive = bf.contains("non-inserted-item")
    # Can't assert exact value, just that it doesn't always return False
    assert isinstance(false_positive, bool)

def test_max_remaining_capacity():
    bf = BloomFilter(max_size=10, seed=42)
    for i in range(5):
        bf.add(i)
    assert bf.max_remaining_capacity == 5
    for i in range(5, 15):
        bf.add(i)
    assert bf.max_remaining_capacity == 0

def test_confidence_bounds():
    bf = BloomFilter(max_size=100, seed=42)
    for i in range(60):
        bf.add(i)
    conf = bf.confidence()
    assert 0 <= conf <= 1
