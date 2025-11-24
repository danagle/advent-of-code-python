# Day 20: Grove Positioning System

def read_input_file(filepath="input.txt"):
    with open("input.txt") as f:
        content = [int(x) for x in f]

    return content


def sum_grove_coordinates(numbers_list, num_mixes):
    length = len(numbers_list)

    # Initialize list of positions (index of elements in the original list)
    positions = list(range(length))

    for _ in range(num_mixes):
        for i, value in enumerate(numbers_list):
            # Find current index of element i
            idx = positions.index(i)
            # Determine the new position
            new_idx = (idx + value) % (length - 1)
            # Move element to new position
            positions.pop(idx)
            positions.insert(new_idx, i)

    # Find the index of zero in final positions
    zero_pos = positions.index(numbers_list.index(0))

    result = sum(
        numbers_list[positions[(zero_pos + offset) % length]] 
        for offset in (1000, 2000, 3000)
    )

    return result


def part_one(encrypted_list):
    mixes = 1
    return sum_grove_coordinates(encrypted_list, mixes)


def part_two(encrypted_list):
    mixes = 10
    decrypted_list = [x * 811589153 for x in encrypted_list]
    return sum_grove_coordinates(decrypted_list, mixes)


if __name__ == "__main__":
    numbers = read_input_file()

    print("Part 1:", part_one(numbers))

    print("Part 2:", part_two(numbers))
