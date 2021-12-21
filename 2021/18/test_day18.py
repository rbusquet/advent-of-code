import functools

from day18 import add, magnitude


def test_add() -> None:
    assert add("[1,2]", "[[3,4],5]") == "[[1,2],[[3,4],5]]"


def test_complex_addition() -> None:
    expected = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    assert expected == add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]")


def test_multi_addition() -> None:
    numbers = """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""".strip().split(
        "\n"
    )

    result = functools.reduce(add, numbers)
    expected = "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    assert result == expected


def test_magnitude() -> None:
    assert magnitude("[[1,2],[[3,4],5]]") == 143
    assert magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
    assert magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]") == 445
    assert magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]") == 791
    assert magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]") == 1137
    assert magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]") == 3488
