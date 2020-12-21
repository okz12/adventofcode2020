from collections import Counter
from typing import List, Tuple, Dict

INGREDIENTS = List[str]
ALLERGENS = List[str]
LINE = Tuple[INGREDIENTS, ALLERGENS]


def parse_line(line: str) -> LINE:
    ingredients, allergens = line.replace(",", "").split(" (contains ", 1)
    return ingredients.split(), allergens[:-1].split()


def match_allergens(
    all_ingredients: INGREDIENTS, all_allergens: ALLERGENS, lines: List[LINE]
) -> Dict[str, str]:
    allergen_matched = {}  # matched
    allergen_dict = {x: set(all_ingredients) for x in all_allergens}
    for ingrs_, allers_ in lines:
        for a in allers_:
            allergen_dict[a] = allergen_dict[a].intersection(set(ingrs_))

    removed = True
    while removed:
        removed = False
        to_remove = set()
        for a in list(allergen_dict.keys()):
            if len(allergen_dict[a]) == 1:
                allergen_matched[a] = list(allergen_dict[a])[0]
                to_remove.add(list(allergen_dict[a])[0])
                del allergen_dict[a]
                removed = True
        for a in list(allergen_dict.keys()):
            allergen_dict[a] = allergen_dict[a].difference(to_remove)
    return allergen_matched


def AllergenMapper(string: str) -> Tuple[int, str]:
    lines = list(map(parse_line, string.split("\n")))
    ingr_counts = Counter([x for y in list(zip(*lines))[0] for x in y])
    all_ingredients = list(ingr_counts.keys())
    all_allergens = list(set([x for y in list(zip(*lines))[1] for x in y]))
    allergen_matched = match_allergens(all_ingredients, all_allergens, lines)

    allergen_free = set(all_ingredients).difference(set(allergen_matched.values()))
    ingredient_map = {v: k for k, v in allergen_matched.items()}

    return sum(ingr_counts[x] for x in allergen_free), ",".join(
        list(sorted(ingredient_map.keys(), key=ingredient_map.get))
    )


if __name__ == "__main__":

    testcase = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

    with open("input.txt", "r") as f:
        data = f.read()

    assert AllergenMapper(testcase) == (5, "mxmxvkd,sqjhc,fvjkl")
    print(AllergenMapper(data))
