# Lab 7: Fuzz Testing Movie Ticket Pricing

This folder adapts the Lab 7 handout to the movie ticket project in `Lab 6`. The three functions under test are `ticket_price`, `group_discount`, and `snack_combo`.

## Run

```powershell
python -m pip install -r requirements.txt
python processor.py
python -m pytest -q test_processor.py
```

The Hypothesis tests generate valid and malformed inputs, check stable pricing properties, and verify that invalid inputs fail with clear exceptions. `processor.py` is the hardened implementation. See `Lab7_FuzzTesting_Report.pdf` for the lab evidence and findings.
