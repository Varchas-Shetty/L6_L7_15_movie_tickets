import pytest

from movie_tickets import group_discount, snack_combo, ticket_price


@pytest.mark.parametrize(
    ("seat", "age", "hour", "weekend", "expected"),
    [
        ("regular", 25, 15, False, 150),
        ("premium", 25, 10, True, 240),
        ("recliner", 25, 20, True, 470),
        ("regular", 25, 11, False, 100),
        ("regular", 25, 18, False, 180),
        ("regular", 25, 17, False, 150),
        ("regular", 25, 15, True, 190),
        ("regular", 2, 15, False, 0),
        ("regular", 3, 15, False, 75),
        ("regular", 12, 15, False, 75),
        ("regular", 13, 15, False, 150),
        ("regular", 59, 15, False, 150),
        ("regular", 60, 15, False, 75),
    ],
)
def test_ticket_price_valid_combinations(seat, age, hour, weekend, expected):
    assert ticket_price(seat, age, hour, weekend) == expected


@pytest.mark.parametrize("seat", ["vip", ""])
def test_ticket_price_rejects_unknown_seat(seat):
    with pytest.raises(ValueError, match="unknown seat"):
        ticket_price(seat, 25, 15, False)


@pytest.mark.parametrize("hour", [-1, 24])
def test_ticket_price_rejects_out_of_range_show_time(hour):
    with pytest.raises(ValueError, match="invalid show time"):
        ticket_price("regular", 25, hour, False)


@pytest.mark.parametrize(
    ("tickets", "student", "expected"),
    [(1, False, 0), (4, True, 0), (5, False, 10), (9, True, 15),
     (10, False, 15), (10, True, 20)],
)
def test_group_discount_valid_tiers(tickets, student, expected):
    assert group_discount(tickets, student) == expected


@pytest.mark.parametrize("tickets", [0, -1])
def test_group_discount_rejects_nonpositive_ticket_count(tickets):
    with pytest.raises(ValueError, match="no tickets"):
        group_discount(tickets, False)


@pytest.mark.parametrize(
    ("size", "coupon", "expected"),
    [("small", False, 120), ("small", True, 70),
     ("medium", False, 180), ("medium", True, 130),
     ("large", False, 250), ("large", True, 200)],
)
def test_snack_combo_sizes_and_coupon(size, coupon, expected):
    assert snack_combo(size, coupon) == expected
