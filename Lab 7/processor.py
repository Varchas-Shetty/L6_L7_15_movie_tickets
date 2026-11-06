"""Hardened movie ticket pricing functions for the Lab 7 fuzzing exercise."""

SEAT_PRICE = {"regular": 150, "premium": 250, "recliner": 400}


def _require_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")


def _require_bool(value, name):
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a boolean")


def ticket_price(seat, age, show_hour, is_weekend):
    if not isinstance(seat, str):
        raise TypeError("seat must be a string")
    if seat not in SEAT_PRICE:
        raise ValueError("unknown seat")
    _require_int(age, "age")
    _require_int(show_hour, "show_hour")
    _require_bool(is_weekend, "is_weekend")
    if age < 0:
        raise ValueError("age must be non-negative")
    if not 0 <= show_hour <= 23:
        raise ValueError("invalid show time")

    price = SEAT_PRICE[seat]
    if show_hour < 12:
        price -= 50
    elif show_hour >= 18:
        price += 30
    if is_weekend:
        price += 40
    if age < 3:
        return 0
    if age <= 12 or age >= 60:
        price //= 2
    return price


def group_discount(tickets, is_student_group):
    _require_int(tickets, "tickets")
    _require_bool(is_student_group, "is_student_group")
    if tickets < 1:
        raise ValueError("no tickets")
    discount = 15 if tickets >= 10 else 10 if tickets >= 5 else 0
    if is_student_group and discount > 0:
        discount += 5
    return discount


def snack_combo(size, has_coupon):
    if not isinstance(size, str):
        raise TypeError("size must be a string")
    if size not in {"small", "medium", "large"}:
        raise ValueError("unknown snack size")
    _require_bool(has_coupon, "has_coupon")
    cost = {"small": 120, "medium": 180, "large": 250}[size]
    return cost - 50 if has_coupon else cost


if __name__ == "__main__":
    print("Ticket price:", ticket_price("regular", 25, 15, False))
    print("Group discount:", group_discount(5, True))
    print("Snack combo:", snack_combo("medium", True))
