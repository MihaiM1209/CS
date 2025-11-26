#!/usr/bin/env python3

import random



E_TABLE = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]



S_BOXES = [

    [
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
        [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
        [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
        [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]
    ],

    [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
        [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]
    ],

    [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
        [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
        [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]
    ],

    [
        [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
        [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
        [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
        [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]
    ],

    [
        [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
        [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
        [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
        [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]
    ],

    [
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
        [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
        [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
        [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]
    ],

    [
        [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
        [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
        [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
        [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]
    ],

    [
        [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
        [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
        [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
        [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]
    ]
]


def display_e_table():
    print("\n" + "=" * 60)
    print("Expansion Permutation Table E (32 bits -> 48 bits)")
    print("=" * 60)
    print("Input position -> Output position")
    for i in range(0, 48, 6):
        row = [f"{E_TABLE[j]:2d}" for j in range(i, i + 6)]
        print("  ".join(row))
    print()


def display_s_box(s_box_num):
    s_box = S_BOXES[s_box_num - 1]
    print(f"\n{'=' * 60}")
    print(f"S-box S{s_box_num} (6 bits input -> 4 bits output)")
    print("=" * 60)
    print("Row determined by first and last bits of 6-bit input")
    print("Column determined by middle 4 bits of 6-bit input")
    print("\n        Column (middle 4 bits)")
    print("Row     0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15")
    print("-" * 60)
    for row_idx, row in enumerate(s_box):
        row_str = f"  {row_idx}   " + "  ".join(f"{val:2d}" for val in row)
        print(row_str)
    print()


def display_all_s_boxes():
    for i in range(1, 9):
        display_s_box(i)


def binary_string(value, length):
    return format(value, f'0{length}b')


def hex_string(value, length):
    return format(value, f'0{length}X')


def input_48_bits():
    print("\n" + "=" * 60)
    print("Input: Ki + E(Ri-1) = 48 bits")
    print("=" * 60)
    print("1. Enter 48-bit value manually (as binary or hexadecimal)")
    print("2. Generate random 48-bit value")

    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == '1':
        print("\nEnter the 48-bit value:")
        print("Format options:")
        print("  - Binary: 48 bits (e.g., 011000010001011110111010100101100101100110100011)")
        print("  - Hexadecimal: 12 hex digits (e.g., 0x6145EBA5969A3)")

        value_input = input("Enter value: ").strip()


        if value_input.startswith('0x') or value_input.startswith('0X'):
            value_input = value_input[2:]
            try:
                value = int(value_input, 16)
                binary = binary_string(value, 48)
            except ValueError:
                print("Invalid hexadecimal input!")
                return None
        else:

            try:
                value = int(value_input, 2)
                if len(value_input) != 48:
                    print(f"Warning: Input length is {len(value_input)}, padding to 48 bits")
                    binary = value_input.zfill(48) if len(value_input) < 48 else value_input[:48]
                else:
                    binary = value_input
            except ValueError:
                print("Invalid binary input!")
                return None
    else:

        value = random.getrandbits(48)
        binary = binary_string(value, 48)
        print(f"\nGenerated random 48-bit value:")
        print(f"Binary:  {binary}")
        print(f"Hex:     0x{hex_string(value, 12)}")

    return binary


def split_48_bits(bits_48):
    blocks = []
    for i in range(8):
        start = i * 6
        end = start + 6
        blocks.append(bits_48[start:end])
    return blocks


def apply_s_box(block_6bits, s_box_num):

    row_bits = block_6bits[0] + block_6bits[5]
    row = int(row_bits, 2)


    col_bits = block_6bits[1:5]
    col = int(col_bits, 2)


    s_box = S_BOXES[s_box_num - 1]
    value = s_box[row][col]

    return row, col, value, binary_string(value, 4)


def solve_problem_2_9():
    print("\n" + "=" * 70)
    print("DES Algorithm - Problem 2.9")
    print("=" * 70)
    print("Given: Ki + E(Ri-1) = 48 bits")
    print("Task: Determine Sj(Bj) for a given j")
    print("=" * 70)


    print("\n" + "=" * 70)
    print("DES TABLES")
    print("=" * 70)

    display_e_table()


    bits_48 = input_48_bits()
    if bits_48 is None:
        return


    print("\n" + "=" * 70)
    print("STEP 1: Input Analysis")
    print("=" * 70)
    print(f"Ki + E(Ri-1) = {bits_48}")
    print(f"Length: {len(bits_48)} bits")
    print(f"Hex: 0x{hex_string(int(bits_48, 2), 12)}")


    blocks = split_48_bits(bits_48)

    print("\n" + "=" * 70)
    print("STEP 2: Split into 8 blocks of 6 bits each")
    print("=" * 70)
    for i, block in enumerate(blocks):
        print(f"B{i+1} = {block} (binary) = {int(block, 2):2d} (decimal)")


    print("\n" + "=" * 70)
    print("STEP 3: Select S-box")
    print("=" * 70)
    while True:
        try:
            j = int(input("Enter j (S-box number 1-8): ").strip())
            if 1 <= j <= 8:
                break
            else:
                print("Please enter a number between 1 and 8.")
        except ValueError:
            print("Please enter a valid number.")


    display_s_box(j)


    print("\n" + "=" * 70)
    print(f"STEP 4: Apply S-box S{j} to block B{j}")
    print("=" * 70)

    block_bj = blocks[j - 1]
    print(f"B{j} = {block_bj} (6 bits)")

    row, col, value, output = apply_s_box(block_bj, j)

    print(f"\nDetailed calculation:")
    print(f"  - First bit:  {block_bj[0]}")
    print(f"  - Last bit:   {block_bj[5]}")
    print(f"  - Row bits:   {block_bj[0]}{block_bj[5]} = {int(block_bj[0] + block_bj[5], 2)} (decimal)")
    print(f"  - Row:        {row}")
    print(f"  - Middle 4 bits: {block_bj[1:5]}")
    print(f"  - Column:     {int(block_bj[1:5], 2)} (decimal)")
    print(f"  - Lookup S{j}[{row}][{col}] = {value}")
    print(f"  - Output:     {output} (4 bits) = {value} (decimal)")

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)
    print(f"S{j}(B{j}) = {output} (binary) = {value} (decimal) = 0x{hex_string(value, 1)} (hex)")


    print("\n" + "=" * 70)
    print("BONUS: All S-box outputs")
    print("=" * 70)
    all_outputs = []
    for i in range(8):
        _, _, val, out = apply_s_box(blocks[i], i + 1)
        all_outputs.append(out)
        print(f"S{i+1}(B{i+1}) = {out} (decimal: {val})")

    print(f"\nCombined 32-bit output: {''.join(all_outputs)}")
    print(f"Hex: 0x{hex_string(int(''.join(all_outputs), 2), 8)}")


def main():
    try:
        while True:
            solve_problem_2_9()

            print("\n" + "=" * 70)
            choice = input("Do you want to solve another problem? (y/n): ").strip().lower()
            if choice not in ['y', 'yes']:
                break

        print("\nThank you for using DES Algorithm Implementation!")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

