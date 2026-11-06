"""Property based fuzz tests for the input validation and pricing functions."""

import pytest
from hypothesis import given, strategies as st

from processor import group_discount, snack_combo, ticket_price


@given(
    seat=st.sampled_from(["regular", "premium", "recliner"]),
    age=st.integers(min_value=0, max_value=120),
    hour=st.integers(min_value=0, max_value=23),
    weekend=st.booleans(),
)
def test_ticket_price_is_nonnegative_and_deterministic(seat, age, hour, weekend):
    result = ticket_price(seat, age, hour, weekend)
    assert result >= 0
    assert ticket_price(seat, age, hour, weekend) == result


@given(age=st.integers(max_value=-1))
def test_negative_age_rejected(age):
    with pytest.raises(ValueError):
        ticket_price("regular", age, 12, False)


@given(hour=st.one_of(st.integers(max_value=-1), st.integers(min_value=24)))
def test_invalid_hours_rejected(hour):
    with pytest.raises(ValueError, match="invalid show time"):
        ticket_price("regular", 25, hour, False)


@given(value=st.one_of(st.none(), st.text(), st.floats(allow_nan=True, allow_infinity=True), st.booleans()))
def test_ticket_numeric_arguments_reject_wrong_types(value):
    with pytest.raises(TypeError):
        ticket_price("regular", value, 12, False)


@given(tickets=st.integers(min_value=1, max_value=10000), student=st.booleans())
def test_group_discount_in_valid_range(tickets, student):
    result = group_discount(tickets, student)
    assert result in ({0, 10, 15} if not student else {0, 15, 20})


@given(tickets=st.integers(max_value=0))
def test_nonpositive_groups_rejected(tickets):
    with pytest.raises(ValueError, match="no tickets"):
        group_discount(tickets, False)


@given(tickets=st.one_of(st.none(), st.text(), st.floats(), st.booleans()))
def test_invalid_group_count_types_rejected(tickets):
    with pytest.raises(TypeError):
        group_discount(tickets, False)


@given(size=st.sampled_from(["small", "medium", "large"]), coupon=st.booleans())
def test_snack_combo_known_sizes(size, coupon):
    cost = snack_combo(size, coupon)
    assert cost > 0
    assert cost == snack_combo(size, coupon)


@given(size=st.text().filter(lambda s: s not in {"small", "medium", "large"}))
def test_unknown_snack_sizes_rejected(size):
    with pytest.raises(ValueError, match="unknown snack size"):
        snack_combo(size, False)


@given(size=st.one_of(st.none(), st.integers(), st.lists(st.integers())))
def test_non_string_snack_sizes_rejected(size):
    with pytest.raises(TypeError, match="size must be a string"):
        snack_combo(size, False)


@pytest.mark.parametrize("value", [None, 0, 1, "yes", []])
def test_boolean_flags_reject_non_booleans(value):
    with pytest.raises(TypeError):
        group_discount(5, value)
    with pytest.raises(TypeError):
        snack_combo("small", value)
