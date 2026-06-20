import calendar
from datetime import date, timedelta


def pay_for_shift(position):
    paid_hours = 11.5
    base_rate = 16.64
    premium_rate = 18.64

    if position <= 4:
        rate = base_rate
    else:
        rate = premium_rate

    return rate * paid_hours


def total_for_run(num_shifts):
    total = 0
    for position in range(1, num_shifts + 1):
        total += pay_for_shift(position)
    return total


def pay_day(start_date):
    weekday = start_date.weekday()

    if weekday == 6:  # Sunday
        days_to_saturday = 6
    else:
        days_to_saturday = 5 - weekday

    week_end_saturday = start_date + timedelta(days=days_to_saturday)
    return week_end_saturday + timedelta(days=6)


def assign_positions(dates):
    dates = sorted(dates)
    result = []
    position = 0
    previous = None

    for d in dates:
        if previous is not None and d == previous + timedelta(days=1):
            position += 1
        else:
            position = 1
        result.append((d, position))
        previous = d

    return result


def weekly_totals(dates):
    shifts = assign_positions(dates)
    totals = {}

    for d, position in shifts:
        friday = pay_day(d)
        pay = pay_for_shift(position)

        if friday in totals:
            totals[friday] = totals[friday] + pay
        else:
            totals[friday] = pay

    return totals


def income_tax(annual_income):
    personal_allowance = 12570
    higher_threshold = 50270
    additional_threshold = 125140

    tax = 0

    basic_band = max(0, min(annual_income, higher_threshold) - personal_allowance)
    tax = tax + basic_band * 0.20

    higher_band = max(0, min(annual_income, additional_threshold) - higher_threshold)
    tax = tax + higher_band * 0.40

    additional_band = max(0, annual_income - additional_threshold)
    tax = tax + additional_band * 0.45

    return tax


def national_insurance(weekly_gross):
    primary_threshold = 242
    upper_earnings_limit = 967

    main_band = max(0, min(weekly_gross, upper_earnings_limit) - primary_threshold)
    upper_band = max(0, weekly_gross - upper_earnings_limit)

    ni = main_band * 0.08 + upper_band * 0.02
    return ni


def weekly_take_home(weekly_gross):
    annual_income = weekly_gross * 52
    tax = income_tax(annual_income) / 52
    ni = national_insurance(weekly_gross)
    net = weekly_gross - tax - ni

    return {"gross": weekly_gross, "tax": tax, "ni": ni, "net": net}


def weekly_breakdown(dates):
    totals = weekly_totals(dates)
    breakdown = {}

    for friday, gross in totals.items():
        breakdown[friday] = weekly_take_home(gross)

    return breakdown


def monthly_totals(dates, year, month):
    breakdown = weekly_breakdown(dates)
    total = {"gross": 0, "tax": 0, "ni": 0, "net": 0}

    for friday, pay in breakdown.items():
        if friday.year == year and friday.month == month:
            total["gross"] = total["gross"] + pay["gross"]
            total["tax"] = total["tax"] + pay["tax"]
            total["ni"] = total["ni"] + pay["ni"]
            total["net"] = total["net"] + pay["net"]

    return total
