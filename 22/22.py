from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from typing import List, Set

@dataclass
class Combat:
    p1: List[int]
    p2: List[int]
    history: Set
    game: int
    round: int = 1

    @staticmethod
    def parse(string: str, game: int = 1) -> Combat:
        p1_, p2_ = [deque(map(int, p.split("\n")[1:])) for p in string.split("\n\n", 1)]
        return Combat(p1_, p2_, set(), game)

    def round_(self):
        print(
        f"""-- Round {self.round} Game {self.game}--\n\
Player 1's deck: {self.p1}\n\
Player 2's deck: {self.p2}\n\
Player 1 plays: {self.p1[0]}\n\
Player 2 plays: {self.p2[0]}\n\
Player {1 if self.p1[0]>self.p2[0] else 2} wins the round!\n"""
        )

        if self.p1[0] > self.p2[0]:
            self.p1.append(self.p1.popleft())
            self.p1.append(self.p2.popleft())
        else:
            self.p2.append(self.p2.popleft())
            self.p2.append(self.p1.popleft())
        self.round += 1
        self.history.add((tuple(self.p1), tuple(self.p2)))

    def run(self) -> int:
        while self.p1 and self.p2:
            if (tuple(self.p1), tuple(self.p2)) in self.history:
                print("P1 wins")
            self.round_()
        def score(A: List[int]):
            return sum((len(A)-i) * val for i, val in enumerate(A))
        return score(self.p1) if self.p1 else score(self.p2)

if __name__ == "__main__":
    testcase = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

    with open('input.txt', 'r') as f:
        data = f.read()

    assert Combat.parse(testcase).run() == 306
    print (Combat.parse(data).run())

# If previously spotted decks = p1 wins
# Draw top deck and len(deck) < top-card-value - higher wins
# else


