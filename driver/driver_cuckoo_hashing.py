from structures.cuckoo_hashing import CuckooHashTable

def show_tables(table1, table2):
    snapshot1 = [str(item) if item is not None else "None" for item in table1]
    snapshot2 = [str(item) if item is not None else "None" for item in table2]
    print("Tabla1: [" + " ".join(snapshot1) + "]")
    print("Tabla2: [" + " ".join(snapshot2) + "]\n")

def main():
    keys = ["ariana", "camila", "diego", "akira", "sandro", "amir", "albert", "alfredo", "omar", "luis"]
    cuckoo = CuckooHashTable(size=20, max_displacements=9)

    for key in keys:
        print(f"Adding: {key}")
        h1 = cuckoo.hash1.hash(key) % cuckoo.size
        h2 = cuckoo.hash2.hash(key) % cuckoo.size
        print(f"h1: {h1}, h2: {h2}")

        displaced = key
        current_table = 1  

        for i in range(cuckoo.max_displacements):
            if current_table == 1:
                pos = cuckoo._position(displaced, 1)
                if cuckoo.table1[pos] is None:
                    cuckoo.table1[pos] = displaced
                    print(f"Inserted {displaced} at position table1[{pos}]")
                    break
                print(f"Displacing {cuckoo.table1[pos]} from table1[{pos}] with {displaced}")
                displaced, cuckoo.table1[pos] = cuckoo.table1[pos], displaced
                current_table = 2
            else:
                pos = cuckoo._position(displaced, 2)
                if cuckoo.table2[pos] is None:
                    cuckoo.table2[pos] = displaced
                    print(f"Inserted {displaced} at position table2[{pos}]")
                    break
                print(f"Displacing {cuckoo.table2[pos]} from table2[{pos}] with {displaced}")
                displaced, cuckoo.table2[pos] = cuckoo.table2[pos], displaced
                current_table = 1
        else:
            print(f"Failed to insert {key} after max displacements")

        show_tables(cuckoo.table1, cuckoo.table2)

    print("Membership checks:")
    test_keys = ["ariana", "camila", "diego", "akira", "sandro", "alfredo", "amir", "albert", "omar", "luis"]
    for key in test_keys:
        result = cuckoo.contains(key)
        status = "Found in table" if result else "Not found"
        print(f"  {key:>8}: {status}")

    print("\nFinal state of tables:")
    show_tables(cuckoo.table1, cuckoo.table2)

if __name__ == "__main__":
    main()

