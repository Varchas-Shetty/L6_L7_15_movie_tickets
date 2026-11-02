import pytest

from movie_tickets import group_discount, snack_combo, ticket_price


@pytest.mark.parametrize(
    ("seat", "age", "hour", "weekend", "expected"),
    [
        ("regular", 2, 11, False, 0),   # child return, morning branch
        ("regular", 3, 11, False, 50),  # child boundary and morning true
        ("regular", 12, 12, True, 95),  # child discount, noon boundary, weekend
        ("regular", 13, 17, False, 150),
        ("regular", 59, 18, False, 180), # evening, age OR false
        ("regular", 60, 18, True, 110), # senior age OR true, weekend
        ("premium", 25, 17, False, 250),
        ("recliner", 25, 18, False, 430),
    ],
)
def test_ticket_price_decision_outcomes(seat, age, hour, weekend, expected):
    assert ticket_price(seat, age, hour, weekend) == expected


@pytest.mark.parametrize("seat", ["", "box"])
def test_unknown_seat_branch(seat):
    with pytest.raises(ValueError, match="unknown seat"):
        ticket_price(seat, 25, 15, False)


@pytest.mark.parametrize("hour", [-1, 24])
def test_invalid_time_branches(hour):
    with pytest.raises(ValueError, match="invalid show time"):
        ticket_price("regular", 25, hour, False)


@pytest.mark.parametrize(
    ("tickets", "student", "expected"),
    [
        (1, False, 0),   # lower tier, student false
        (4, True, 0),    # lower tier, student true but no discount
        (5, False, 10),  # middle threshold
        (9, True, 15),   # student addition to middle tier
        (10, False, 15), # upper threshold
        (12, True, 20),  # student addition to upper tier
    ],
)
def test_group_discount_decisions(tickets, student, expected):
    assert group_discount(tickets, student) == expected


@pytest.mark.parametrize("tickets", [0, -1])
def test_invalid_group_count_branches(tickets):
    with pytest.raises(ValueError, match="no tickets"):
        group_discount(tickets, False)


@pytest.mark.parametrize(
    ("size", "coupon", "expected"),
    [("small", False, 120), ("small", True, 70),
     ("medium", False, 180), ("medium", True, 130),
     ("large", False, 250), ("large", True, 200),
     ("extra-large", False, 250)],
)
def test_snack_size_and_coupon_branches(size, coupon, expected):
    assert snack_combo(size, coupon) == expected

