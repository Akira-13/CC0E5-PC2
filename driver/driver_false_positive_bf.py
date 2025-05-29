from os import urandom
from structures.tabulated_bloom_filter import BloomFilter
import matplotlib.pyplot as plt

# Lists to collect plotting data
empirical_rates = []
theoretical_rates = []
inserted_counts = []


# Tracking statistics
false_positives = 0
test_queries_per_batch = 100000
added_items = []
batch_size = 100
bf_size = 1000
queries = 0

# Initialize Bloom filter
bf = BloomFilter(max_size=bf_size, max_tolerance=0.01, seed=42)

# Run until 1000 unique elements have been inserted
while len(added_items) < bf_size:
    # Insert 100 pseudorandom 8-byte items
    for _ in range(batch_size):
        item = urandom(8)
        added_items.append(item)
        bf.add(item)

    # Query 100000 fresh random items not inserted
    for _ in range(test_queries_per_batch):
        test_item = urandom(8)
        while test_item in added_items:
            test_item = urandom(8)
        if bf.contains(test_item):
            false_positives += 1

    empirical_fpr = false_positives / test_queries_per_batch
    theoretical_fpr = bf.false_positive_probability()

    print(f"\nItems inserted so far: {len(added_items)}")
    print(f"Empirical false positive rate: {empirical_fpr:.6f}")
    print(f"Theoretical false positive rate: {theoretical_fpr:.6f}")

    inserted_counts.append(len(added_items))
    empirical_rates.append(empirical_fpr)
    theoretical_rates.append(theoretical_fpr)

    false_positives = 0

# Plotting
x = range(len(inserted_counts))
width = 0.35

plt.figure(figsize=(12, 6))
plt.bar([i - width/2 for i in x], empirical_rates, width=width, label='Empirical FPR')
plt.bar([i + width/2 for i in x], theoretical_rates, width=width, label='Theoretical FPR')

plt.xticks(ticks=x, labels=inserted_counts)
plt.xlabel("Items Inserted")
plt.ylabel("False Positive Rate")
plt.title("Comparison of Empirical vs Theoretical False Positive Rates")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("statistics/false_positive_rates_bf_comparison.png", dpi=300)
print("Saved plot to false_positive_rates_comparison.png")
