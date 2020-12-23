from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class Node:
    val: int
    nex: Node = None


# Linked List with Hashmap
class CrabCups:
    def __init__(self, nums: List[int]) -> None:
        self.head = Node(nums[0])
        self.pointer = self.head
        self.hashmap = {self.head.val: self.head}
        curr = self.head
        for val in nums[1:]:
            curr.nex = Node(val)
            curr = curr.nex
            self.hashmap[curr.val] = curr
        curr.nex = self.head  # Circular Linked List
        self.maxval = max(nums)
        del nums

    def move(self) -> None:
        pickup = [
            self.pointer.val,
            self.pointer.nex.val,
            self.pointer.nex.nex.val,
            self.pointer.nex.nex.nex.val,
        ]

        # Find destination label
        dest_label = self.pointer.val - 1 if self.pointer.val != 1 else self.maxval
        while dest_label in pickup:
            dest_label = dest_label - 1 if dest_label != 1 else self.maxval

        # Find destination and pickup nodes
        dest_before, dest_after = self.hashmap[dest_label], self.hashmap[dest_label].nex
        pickup_first, pickup_last, pickup_after = pickup[1], pickup[-1], pickup[-1].nex

        # Move pickup after destination
        self.pointer.nex = pickup_after
        dest_before.nex = pickup_first
        pickup_last.nex = dest_after

        # Move to next element
        self.pointer = self.pointer.nex

    def linearize(self, start) -> List[int]:
        curr = start
        sval = curr.val
        curr = curr.nex

        res = [start.val]
        while curr and curr.val != sval:
            res.append(curr.val)
            curr = curr.nex
        return res

    def __repr__(self) -> str:
        return " ".join(
            f"({x.val}" if self.pointer == x else f"{x}"
            for x in self.linearize(self.head)
        )


def int_to_list(num: int) -> List[int]:
    return list(map(int, list(str(num))))


def part1(num) -> int:
    crabcups = CrabCups(int_to_list(num))
    for _ in range(100):
        crabcups.move()
    out = crabcups.linearize(crabcups.hashmap[1])
    return int("".join(map(str, out[1:])))


def part2(num: int) -> int:
    crabcups = CrabCups(int_to_list(num) + list(range(10, 1000001)))
    for _ in range(10000000):
        crabcups.move()
    return crabcups.hashmap[1].nex.nex.val * crabcups.hashmap[1].nex.val


if __name__ == "__main__":
    testcase = 389125467
    data = 318946572

    assert part1(testcase) == 67384529
    print(part1(data))

    assert part2(testcase) == 149245887792
    print(part2(data))
