import os
import time
import random
import csv
import pandas as pd
import matplotlib.pyplot as plt
from structures.cuckoo_hashing import CuckooHashTable

OUTPUT_DIR = "statistics"
os.makedirs(OUTPUT_DIR, exist_ok=True)

INSERT_CSV = os.path.join(OUTPUT_DIR, "cuckoo_insert_profile.csv")
FAILURE_CSV = os.path.join(OUTPUT_DIR, "cuckoo_failure_vs_load.csv")
SEARCH_CSV = os.path.join(OUTPUT_DIR, "cuckoo_search_profile.csv")

TABLE_SIZES = list(range(100, 10001, 250))
MAX_FAIL_RATIO = 0.1

def generate_keys(n, key_space=10**6):
    return random.sample(range(key_space), n)

def perfilado_cuckoo():
    with open(INSERT_CSV, "w", newline="") as f_insert, \
         open(FAILURE_CSV, "w", newline="") as f_failure, \
         open(SEARCH_CSV, "w", newline="") as f_search:

        insert_writer = csv.writer(f_insert)
        failure_writer = csv.writer(f_failure)
        search_writer = csv.writer(f_search)

        insert_writer.writerow(["table_size", "num_inserted", "avg_insert_time_s"])
        failure_writer.writerow(["table_size", "num_elements", "load_factor", "failure_rate"])
        search_writer.writerow(["table_size", "num_searches", "avg_search_time_s"])

        for table_size in TABLE_SIZES:
            cuckoo = CuckooHashTable(size=table_size, max_displacements=20)
            keys = generate_keys(int(2.5 * table_size))

            insert_times, inserted_keys = [], []
            success_count, fail_count = 0, 0

            for key in keys:
                start = time.perf_counter()
                success = cuckoo.insert(key)
                elapsed = time.perf_counter() - start

                if success:
                    insert_times.append(elapsed)
                    inserted_keys.append(key)
                    success_count += 1
                else:
                    fail_count += 1

                total = success_count + fail_count
                if total > 20 and (fail_count / total) > MAX_FAIL_RATIO:
                    break

            load_factor = success_count / (2 * table_size)
            avg_insert_time = sum(insert_times) / len(insert_times)

            insert_writer.writerow([table_size, success_count, avg_insert_time])
            failure_writer.writerow([table_size, total, round(load_factor, 2), round(fail_count / total, 4)])

            search_times = []
            for key in inserted_keys:
                start = time.perf_counter()
                cuckoo.contains(key)
                elapsed = time.perf_counter() - start
                search_times.append(elapsed)

            avg_search_time = sum(search_times) / len(search_times)
            search_writer.writerow([table_size, len(inserted_keys), avg_search_time])

    print("Perfilado completo: inserción, fallos y búsqueda.")
    print(f"INSERT_CSV = {INSERT_CSV}")
    print(f"FAILURE_CSV = {FAILURE_CSV}")
    print(f"SEARCH_CSV = {SEARCH_CSV}")

def graficar():
    insert_df = pd.read_csv(INSERT_CSV)
    search_df = pd.read_csv(SEARCH_CSV)
    load_df = pd.read_csv(FAILURE_CSV)

    plt.figure()
    plt.plot(insert_df["table_size"], insert_df["avg_insert_time_s"], marker="o", label="insert (average)")
    plt.xlabel("Table Size")
    plt.ylabel("Avg Insert Time (s)")
    plt.title("Cuckoo Hashing: Insert Profiling")
    plt.legend()
    plt.ylim(1e-6, 1e-5)
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cuckoo_insert_profile.png"))
    plt.close()


    plt.figure()
    plt.plot(search_df["table_size"], search_df["avg_search_time_s"], marker="o", color="green", label="search (average)")
    plt.xlabel("Table Size")
    plt.ylabel("Avg Search Time (s)")
    plt.legend()
    plt.title("Cuckoo Hashing: Search Profiling")
    plt.ylim(1e-6, 1e-5)
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cuckoo_search_profile.png"), dpi=300)
    plt.close()

    plt.figure()
    plt.plot(load_df["table_size"], load_df["load_factor"], marker="o", color="purple", label="load factor (average)")
    plt.xlabel("Table Size")
    plt.ylabel("Load Factor")
    plt.legend()
    plt.title("Cuckoo Hashing: Load Factor")
    plt.yticks([0.1 * i for i in range(1, 10)])
    plt.ylim(0.1, 0.9)
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cuckoo_load_factor.png"), dpi=300)
    plt.close()


if __name__ == "__main__":
    perfilado_cuckoo()
    graficar()



