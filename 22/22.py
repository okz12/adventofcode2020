from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from typing import List, Set, Tuple, Deque

DECK = Deque[int]
DECKTUPLE = Tuple[Tuple[int, ...], Tuple[int, ...]]


@dataclass
class Combat:
    p1: DECK
    p2: DECK
    history: Set[DECKTUPLE]
    game: int
    ngames: int
    recurse: bool
    round: int = 1

    @staticmethod
    def parse(string: str, recurse: bool = False) -> Combat:
        p1_, p2_ = [deque(map(int, p.split("\n")[1:])) for p in string.split("\n\n", 1)]
        return Combat(p1_, p2_, set(), 1, 1, recurse)

    @staticmethod
    def subgame(p1: DECK, p2: DECK, game) -> Combat:
        return Combat(p1, p2, set(), game, game, True)

    def round_(self):
#         print(f"""-- Round {self.round} (Game {self.thisgame}) --\n\
# Player 1's deck: {self.p1}\n\
# Player 2's deck: {self.p2}\n\
# Player 1 plays: {self.p1[0]}\n\
# Player 2 plays: {self.p2[0]}""")
        p1c, p2c = self.p1.popleft(), self.p2.popleft()
        if self.recurse and (
            p1c <= len(self.p1) and p2c <= len(self.p2)
        ):  # go recursive # does card include itself in length ???
            self.ngames += 1
            # print(f"\nPlaying a sub-game to determine the winner...\n=== Game {self.game} ===\n")
            new_game = Combat.subgame(
                deque(list(self.p1)[:p1c]), deque(list(self.p2)[:p2c]), self.ngames
            )

            if new_game.run():
                # print(f"\n...anyway, back to game {self.thisgame}.\nPlayer 1 wins round {self.round} of game {self.thisgame}!\n")
                self.p1.append(p1c)
                self.p1.append(p2c)
            else:
                # print(f"\n...anyway, back to game {self.thisgame}.\nPlayer 2 wins round {self.round} of game {self.thisgame}!\n")
                self.p2.append(p2c)
                self.p2.append(p1c)
        else:
            # print(f"Player {1 if p1c>p2c else 2} round {self.round} of game {self.thisgame}!\n")
            if p1c > p2c:
                self.p1.append(p1c)
                self.p1.append(p2c)
            else:
                self.p2.append(p2c)
                self.p2.append(p1c)
        self.round += 1

    def run(self) -> int:
        while self.p1 and self.p2:
            if (tuple(self.p1), tuple(self.p2)) in self.history:  # recursive won
                return True
            self.history.add((tuple(self.p1), tuple(self.p2)))
            self.round_()
        return bool(self.p1)

    def score(self):
        # print(f"""== Post-game results ==\nPlayer 1's: {self.p1} \nPlayer 2's deck: {self.p2}""")
        A = self.p1 if self.p1 else self.p2
        return sum((len(A) - i) * val for i, val in enumerate(A))


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

    with open("input.txt", "r") as f:
        data = f.read()

    tc = Combat.parse(testcase)
    tc.run()
    assert tc.score() == 306
    rc = Combat.parse(data)
    rc.run()
    print(rc.score())

    tc = Combat.parse(testcase, True)
    tc.run()
    assert tc.score() == 291
    rc = Combat.parse(data, True)
    rc.run()
    print(rc.score())
