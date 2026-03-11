def save(file_number, history):
    filename = file_number + ".txt"
    with open(filename, "w") as f:
        full = "\n".join(history)
        f.write(full)


def load(current, file_number):
    filename = file_number + ".txt"
    skip_next = False
    with open(filename) as f:
        for i, line in enumerate(f):
            if skip_next:
                skip_next = False
                continue
            line = line.strip()
            if line in ("save", "load"):
                skip_next = True
                continue
            if i % 2 == 0:
                op = op_map[line]
            else:
                num = float(line)
                current = op(current, num)
    return current


result = 0.0

op_map = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b,
    "-": lambda a, b: a - b,
    "/": lambda a, b: a / b,
    "//": lambda a, b: a // b,
    "%": lambda a, b: a % b,
}

history = []

while True:
    operation_name = input("Enter op symbol: ")
    if operation_name not in op_map and operation_name not in ("save", "load"):
        break
    history.append(operation_name)
    number = input("Enter number: ")
    history.append(number)
    if operation_name == "save":
        save(number, history)
    elif operation_name == "load":
        result = load(result, number)
        print(result)
    else:
        operation = op_map[operation_name]
        result = operation(result, float(number))
        print(result)

print("Done")
