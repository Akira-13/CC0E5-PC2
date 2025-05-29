import time
import random
from structures.cuckoo_hashing import CuckooHashTable

def generate_keys(n, key_space=1000000):
    return random.sample(range(key_space), n)

def main():
    num_elements = 500
    table_size = 601  
    max_displacements = 20

    cuckoo = CuckooHashTable(size=table_size, max_displacements=max_displacements)
    keys = generate_keys(num_elements)

    inserted = 0
    failed = 0
    insert_times = []

    print("== Insertando elementos ==")
    for key in keys:
        start = time.time()
        success = cuckoo.insert(key)
        insert_times.append(time.time() - start)

        if success:
            inserted += 1
        else:
            failed += 1

    print(f"Insertados exitosamente: {inserted}")
    print(f"Fallos de inserción: {failed}")
    print(f"Tasa de fallo: {failed / num_elements * 100:.2f}%")
    print(f"Tiempo promedio de inserción: {sum(insert_times) / len(insert_times):.6f} s")

    print("\n== Probando búsquedas ==")
    found = 0
    search_times = []

    for key in keys:
        start = time.time()
        if cuckoo.contains(key):
            found += 1
        search_times.append(time.time() - start)

    print(f"Búsquedas exitosas: {found} / {num_elements}")
    print(f"Tiempo promedio de búsqueda: {sum(search_times) / len(search_times):.6f} s")

    print("\n== Estado final de la tabla ==")
    print(cuckoo)

if __name__ == "__main__":
    main()
