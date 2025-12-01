import os

input_file_location = os.path.dirname(os.path.realpath(__file__)) + "/input.txt"

dial_position = 50
dial_numbers = list(range(0, 100))
password = 0


def rotate_dial(instruction: str):
    global dial_position
    global dial_numbers

    distance = int(instruction[1:])
    if instruction[0] == "L":
        dial_position = dial_numbers[(dial_position - distance) % len(dial_numbers)]
    elif instruction[0] == "R":
        dial_position = dial_numbers[(dial_position + distance) % len(dial_numbers)]

    return dial_position


def read_instructions(filename: str):
    with open(filename, "r") as file:
        instructions = file.readlines()
    return [line.strip() for line in instructions]


def decode_password(instructions):
    global password
    for instruction in instructions:
        position = rotate_dial(instruction)
        if position == 0:
            password += 1

    return password


def main():
    instructions = read_instructions(input_file_location)
    password = decode_password(instructions)
    print(f"The decoded password is: {password}")


if __name__ == "__main__":
    main()
