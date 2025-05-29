"""Driver to analyze the uniformity of following tabulation hashes:
- Simple Tabulation Hash
- Twisted Tabulation Hash
- Double Tabulation Hash

It is expected that these hashes follow a closely uniform distribution.
To check this, Pearson's chi-squared test (implementend in scipy.stats) is used.

A number of of buckets is maintained and a random set of data is hashed.
The hashes are indexed in the buckets, which count the number of times a hash has
fallen in this bucket.
If it's uniform, once all elements have been added, it should theoritically have
the number of elements divided by the number of buckets as value in each bucket.
This theoretical result is compared with the real one with Pearson's chi-squared test.

This chi-square statistics should remain around the number of buckets - 1.
In other words, on average the chi-squared statistic should be in the range of NUM_BUCKETS - 1

The p-value shouldn't fall under 0.05. If it falls it indicates the data might not be
uniformly distributed.

The results are saved in statistics/
"""
from os import urandom
from tabulation_hashes import TabulationHash, DoubleTabulationHash, TwistedTabulationHash
from scipy.stats import chisquare
import matplotlib.pyplot as plt

NUM_RUNS = 100
SAMPLE_SIZE = 100000
NUM_BUCKETS = 1000


def plot_stats(stats, pvals, file_name, title):
    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Chi-square statistics
    axs[0].plot(range(1, NUM_RUNS + 1), stats, marker='o', linestyle='-')
    axs[0].axhline(y=NUM_BUCKETS - 1, color='red', linestyle='--', label=f'Expected (df={NUM_BUCKETS-1})')
    axs[0].set_title(f"Chi-Square Statistics ({NUM_RUNS} runs)")
    axs[0].set_xlabel("Run")
    axs[0].set_ylabel("Chi-Square Statistic")
    axs[0].legend()

    # p-values
    axs[1].plot(range(1, NUM_RUNS + 1), pvals, marker='o', linestyle='-')
    axs[1].axhline(y=0.05, color='red', linestyle='--', label='Significance Threshold (0.05)')
    axs[1].set_title(f"p-Values ({NUM_RUNS} Runs)")
    axs[1].set_xlabel("Run")
    axs[1].set_ylabel("p-Value")
    axs[1].legend()

    fig.suptitle(f"Uniformity Test of {title}", fontsize=16)
    plt.tight_layout()
    plt.savefig(f"statistics/{file_name}", dpi=300)
    print(f"Plot saved as {file_name}")

def get_stats(hash_class):
    stats = []
    pvals = []

    for _ in range(NUM_RUNS):
        buckets = [0] * NUM_BUCKETS
        h = hash_class()

        for _ in range(SAMPLE_SIZE):
            s = urandom(8)
            idx = h.hash(s) % NUM_BUCKETS
            buckets[idx] += 1

        stat, p = chisquare(buckets)
        stats.append(stat)
        pvals.append(p)
    return stats, pvals

def main():
    stats, pvals = get_stats(TabulationHash)
    plot_stats(stats, pvals, "simple_tabulation_uniformity_analysis.png", "Tabulation Hashing")

    stats, pvals = get_stats(DoubleTabulationHash)
    plot_stats(stats, pvals, "double_tabulation_uniformity_analysis.png", "Double Tabulation")

    stats, pvals = get_stats(TwistedTabulationHash)
    plot_stats(stats, pvals, "twisted_tabulation_uniformity_analysis.png", "Twisted Tabulation")

if __name__ == '__main__':
    main()
