# Day 16: Packet Decoder

from pathlib import Path
from typing import Tuple, List


def read_input_file(filepath: str = "input.txt") -> str:
    """
    Reads the input file and returns the hexadecimal transmission string.
    """
    return Path(filepath).read_text().strip()


def hex_to_bin(hex_str: str) -> str:
    """
    Converts a hexadecimal string to a binary string, preserving leading zeros.
    """
    return ''.join(f"{int(c, 16):04b}" for c in hex_str)


def parse_packet(bits: str, index: int = 0) -> Tuple[int, int, int]:
    """
    Parses a packet from bits starting at index.
    
    Returns a tuple:
        version_sum: sum of versions in this packet and sub-packets
        value: value of the packet
        next_index: index after this packet
    """
    version = int(bits[index:index + 3], 2)
    type_id = int(bits[index + 3:index + 6], 2)
    i = index + 6
    version_sum = version

    if type_id == 4:  # literal value
        literal_bits = ""
        while True:
            group = bits[i:i + 5]
            literal_bits += group[1:]
            i += 5
            if group[0] == '0':
                break
        value = int(literal_bits, 2)
        return version_sum, value, i
    else:  # operator
        length_type_id = bits[i]
        i += 1
        values: List[int] = []

        if length_type_id == '0':
            total_length = int(bits[i:i + 15], 2)
            i += 15
            end = i + total_length
            while i < end:
                v_sum, val, i = parse_packet(bits, i)
                version_sum += v_sum
                values.append(val)
        else:
            num_subpackets = int(bits[i:i + 11], 2)
            i += 11
            for _ in range(num_subpackets):
                v_sum, val, i = parse_packet(bits, i)
                version_sum += v_sum
                values.append(val)

        # Compute value based on type_id
        if type_id == 0:
            value = sum(values)
        elif type_id == 1:
            value = 1
            for v in values:
                value *= v
        elif type_id == 2:
            value = min(values)
        elif type_id == 3:
            value = max(values)
        elif type_id == 5:
            value = int(values[0] > values[1])
        elif type_id == 6:
            value = int(values[0] < values[1])
        elif type_id == 7:
            value = int(values[0] == values[1])
        else:
            raise ValueError(f"Unknown type_id: {type_id}")

        return version_sum, value, i


def main(filepath: str = "input.txt") -> None:
    hex_data = read_input_file(filepath)
    bits = hex_to_bin(hex_data)
    version_sum, value, _ = parse_packet(bits)
    print(f"Part 1: {version_sum}")
    print(f"Part 2: {value}")


if __name__ == "__main__":
    main()
