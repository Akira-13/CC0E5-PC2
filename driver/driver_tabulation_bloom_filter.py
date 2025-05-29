from structures.tabulated_bloom_filter import BloomFilter
import string

def display_bits(bitarray, total_bits):
    """Visual display of the bit array grouped by byte."""
    bits = []
    for i in range(total_bits):
        byte = bitarray[i // 8]
        bit = (byte >> (i % 8)) & 1
        bits.append(str(bit))
    # Format output as rows of 8 bits
    return ' '.join([''.join(bits[i:i+8]) for i in range(0, len(bits), 8)])

def main():
    elements_to_add = ["apple", "banana", "cherry", "date", "fig"]
    elements_to_check = ["apple", "banana", "grape", "kiwi", "fig"]

    bf = BloomFilter(max_size=10, max_tolerance=0.01, seed=123)
    print("Initial bit array:")
    print(display_bits(bf._bits, bf._num_bits))
    print()

    for el in elements_to_add:
        print(f"Adding: {el}")
        bf.add(el)
        print(display_bits(bf._bits, bf._num_bits))
        print()

    print("Membership checks:")
    for el in elements_to_check:
        result = bf.contains(el)
        print(f"{el:>8}: {'Possibly in set' if result else 'Definitely not in set'}")

    print("\nFinal bit array:")
    print(display_bits(bf._bits, bf._num_bits))
    print(f"\nApproximate number of items inserted: {bf.size}")
    print(f"Estimated false positive probability: {bf.false_positive_probability():.6f}")
    print(f"Confidence (1 - false positive rate): {bf.confidence():.6f}")

if __name__ == "__main__":
    main()
