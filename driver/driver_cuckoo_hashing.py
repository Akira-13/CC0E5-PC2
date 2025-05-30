from structures.cuckoo_hashing import CuckooHashTable

def show_table(table):
    snapshot = [str(item) if item is not None else "None" for item in table]
    print("[" + " ".join(snapshot) + "]\n")

def main():
    keys = ["ariana", "camila", "diego", "akira", "sandro", "amir", "albert", "alfredo", "omar"]
    cuckoo = CuckooHashTable(size=20, max_displacements=9)

    for key in keys:
        print(f"Adding: {key}")
        h1 = cuckoo.hash1.hash(key) % cuckoo.size
        h2 = cuckoo.hash2.hash(key) % cuckoo.size
        print(f"h1: {h1}, h2: {h2}")

        displaced = key
        for i in range(cuckoo.max_displacements):
            pos1 = cuckoo._position(displaced, 1)
            if cuckoo.table[pos1] is None:
                cuckoo.table[pos1] = displaced
                print(f"Inserted {displaced} at position h1 = {pos1}")
                break

            print(f"Displacing {cuckoo.table[pos1]} from h1 = {pos1} with {displaced}")
            displaced, cuckoo.table[pos1] = cuckoo.table[pos1], displaced

            pos2 = cuckoo._position(displaced, 2)
            if cuckoo.table[pos2] is None:
                cuckoo.table[pos2] = displaced
                print(f"Inserted {displaced} at position h2 = {pos2}")
                break

            print(f"Displacing {cuckoo.table[pos2]} from h2 = {pos2} with {displaced}")
            displaced, cuckoo.table[pos2] = cuckoo.table[pos2], displaced
        else:
            print(f"Failed to insert {key} after max displacements")

        show_table(cuckoo.table)
    
    print("Membership checks")
    test_keys = ["ariana", "camila", "diego", "akira", "sandro", "alfredo", "amir", "albert", "omar"]
    for key in test_keys:
        result = cuckoo.contains(key)
        status = "Found in table" if result else "Not found"
        print(f"  {key:>8}: {status}")

    print("\nFinal table state")
    show_table(cuckoo.table)

if __name__ == "__main__":
    main()
