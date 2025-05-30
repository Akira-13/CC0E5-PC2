import cProfile
import pstats
import random
import unittest
import os
from os import urandom
from structures.tabulated_bloom_filter import BloomFilter

if not os.path.exists('statistics'):
    os.makedirs('statistics', exist_ok=True)

class BloomFilterProfile(unittest.TestCase):
    Sizes = [100, 200, 300, 400, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, \
             10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
    Runs = 1000  # Number of profiling runs for each method and size
    OutputFileName = 'statistics/profile_bf.csv'

    @staticmethod
    def write_header(f) -> None:
        f.write('test_case,filter_size,method_name,total_time,cumulative_time,per_call_time\n')

    @staticmethod
    def write_row(f, test_case: str, filter_size: int, method_name: str,
                   total_time: float, cumulative_time: float, per_call_time: float) -> None:
        f.write(f'{test_case},{filter_size},{method_name},{total_time},{cumulative_time},{per_call_time}\n')

    @staticmethod
    def get_running_times(st: pstats.Stats, method_name: str):
        ps = st.strip_dirs().stats

        def is_bf_method(k):
            return method_name in k[2]

        keys = list(filter(is_bf_method, ps.keys()))
        return [(key[2], ps[key][2], ps[key][3], ps[key][3] / ps[key][1]) for key in keys]

    def test_profile_bloomfilter_add_and_contains(self) -> None:
        with open(BloomFilterProfile.OutputFileName, 'w') as f:
            BloomFilterProfile.write_header(f)

            for size in BloomFilterProfile.Sizes:
                bf = BloomFilter(max_size=size, max_tolerance=0.01, seed=random.randint(1,100))

                # Profile 'add' method
                for _ in range(BloomFilterProfile.Runs):
                    pro = cProfile.Profile()
                    pro.runcall(bf.add, urandom(8))
                    st = pstats.Stats(pro)

                    for method_name, total_time, cumulative_time, per_call_time in \
                            BloomFilterProfile.get_running_times(st, 'add'):
                        BloomFilterProfile.write_row(f, 'bloom', size, method_name,
                                                     total_time, cumulative_time, per_call_time)

                # Profile 'contains' method
                for _ in range(BloomFilterProfile.Runs):
                    pro = cProfile.Profile()
                    pro.runcall(bf.contains, urandom(8))
                    st = pstats.Stats(pro)

                    for method_name, total_time, cumulative_time, per_call_time in \
                            BloomFilterProfile.get_running_times(st, 'contains'):
                        BloomFilterProfile.write_row(f, 'bloom', size, method_name,
                                                     total_time, cumulative_time, per_call_time)


suite = unittest.TestLoader().loadTestsFromTestCase(BloomFilterProfile)
unittest.TextTestRunner(verbosity=2).run(suite)

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv("statistics/profile_bf.csv")

# Group by filter size and method, calculate average per-call time
avg_times = data.groupby(["filter_size", "method_name"])["per_call_time"].mean().unstack()

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(avg_times.index, avg_times["add"], marker='o', label="Add (average)")
plt.plot(avg_times.index, avg_times["contains"], marker='o', label="Contains (average)")

plt.xlabel("Bloom Filter Size")
plt.ylabel("Average Time per Call (seconds)")
plt.title("Average Time per Call for add() and contains() by Bloom Filter Size")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Save the plot
plt.savefig("statistics/profile_average_bf_plot.png", dpi=300)
print("Saved plot to bloom_filter_avg_times.png")
