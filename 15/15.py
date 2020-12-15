from typing import List

def spoken(A: List[int], num: int = 2020):
    memory, curr = {v: i for i, v in enumerate(A)}, 0
    for i in range(len(A), num-1):
        memory[curr], curr = i, i - memory.get(curr, i) #0 if not in spoken
    return curr

if __name__ == "__main__":
    data = [16, 11, 15, 0, 1, 7]

    assert spoken([0, 3, 6]) == 436
    assert spoken([1, 3, 2]) == 1
    assert spoken([2, 1, 3]) == 10
    assert spoken([1, 2, 3]) == 27
    assert spoken([2, 3, 1]) == 78
    assert spoken([3, 2, 1]) == 438
    assert spoken([3, 1, 2]) == 1836
    print(spoken(data))

    assert spoken([0, 3, 6], 30000000) == 175594
    assert spoken([1, 3, 2], 30000000) == 2578
    assert spoken([2, 1, 3], 30000000) == 3544142
    assert spoken([1, 2, 3], 30000000) == 261214
    assert spoken([2, 3, 1], 30000000) == 6895259
    assert spoken([3, 2, 1], 30000000) == 18
    assert spoken([3, 1, 2], 30000000) == 362
    print(spoken(data, 30000000))