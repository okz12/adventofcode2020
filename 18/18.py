import operator
import re

commands = {"+": operator.add, "*": operator.mul}
parse = lambda string: list(re.findall(r"\d+|\*|\+", string))


def eval_brackets(string: str, pos_first: bool = False) -> int:
    if pos_first:
        while m := re.search(r"\d+\s\+\s\d+", string):
            string = string[: m.start()] + str(eval_brackets(m[0])) + string[m.end():]
    stack = parse(string)[::-1]
    val = int(stack.pop())
    while stack:
        op = commands[stack.pop()]
        val = op(val, int(stack.pop()))
    return val


def eval_expression(string: str, pos_first: bool = False) -> int:
    while m := re.search(r"\([\d\s\+\*]+\)", string):
        string = (
            string[: m.start()] + str(eval_brackets(m[0], pos_first)) + string[m.end():]
        )
    return eval_brackets(string, pos_first)


if __name__ == "__main__":
    testcases = [
        "1 + (2 * 3) + (4 * (5 + 6))",
        "2 * 3 + (4 * 5)",
        "5 + (8 * 3 + 9 + 3 * 4 * 3)",
        "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
        "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",
    ]

    with open("input.txt", "r") as f:
        data = f.read()

    assert eval_expression(testcases[0]) == 51
    assert eval_expression(testcases[1]) == 26
    assert eval_expression(testcases[2]) == 437
    assert eval_expression(testcases[3]) == 12240
    assert eval_expression(testcases[4]) == 13632

    print(sum(eval_expression(x) for x in data.split("\n")))

    assert eval_expression(testcases[0], pos_first=True) == 51
    assert eval_expression(testcases[1], pos_first=True) == 46
    assert eval_expression(testcases[2], pos_first=True) == 1445
    assert eval_expression(testcases[3], pos_first=True) == 669060
    assert eval_expression(testcases[4], pos_first=True) == 23340

    print(sum(eval_expression(x, pos_first=True) for x in data.split("\n")))
