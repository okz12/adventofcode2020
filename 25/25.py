def find_loop_size(encryption_key: int) -> int:
    value = 1
    subject_number = 7
    loop_size = 0
    while value != encryption_key:
        value = (value * subject_number) % 20201227
        loop_size += 1
    return loop_size


def create(loop_size: int, subject_number: int) -> int:
    value = 1
    for _ in range(loop_size):
        value = (value * subject_number) % 20201227
    return value


if __name__ == "__main__":
    testcase = (17807724, 5764801)
    data = (16915772, 18447943)

    assert create(find_loop_size(testcase[0]), testcase[1]) == 14897079
    print(create(find_loop_size(data[0]), data[1]))
