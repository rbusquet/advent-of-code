from day18 import addition


def test_addition() -> None:
    assert addition((1, 2), ((3, 4), 5)) == ((1, 2), ((3, 4), 5))


def test_complex_addition() -> None:
    left = ((((4, 3), 4), 4), (7, ((8, 4), 9)))
    right = (1, 1)
    expected = ((((0, 7), 4), ((7, 8), (6, 0))), (8, 1))
    assert addition(left, right) == expected
