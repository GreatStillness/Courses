starting_salary = float(input("Enter your starting salary: "))
salary = starting_salary
semi_annual_rise = 0.07
r = 0.04

total_cost = 1_000_000
portion_down_payment = 0.25
required_amount = total_cost * portion_down_payment

fraction_saved_low = 0
fraction_saved_high = 1
months = 36
steps = 0
fraction_saved = (fraction_saved_low + fraction_saved_high) / 2
portion_saved = salary / 12 * fraction_saved
search_steps = 0


def get_amount(salary_argument, fraction_saved_argument):
    savings = 0
    portion = salary_argument / 12 * fraction_saved_argument
    for m in range(1, months + 1):
        savings += savings * r / 12 + portion
        if m % 6 == 0:
            salary_argument *= 1 + semi_annual_rise
            portion = salary_argument / 12 * fraction_saved_argument
    return savings


if get_amount(starting_salary, fraction_saved) < required_amount:
    print("It is not possible to pay the down payment in three years.")
    exit()

while True:
    search_steps += 1
    amount = get_amount(starting_salary, fraction_saved)

    if abs(amount - required_amount) <= 100:
        print(f"Best savings rate: {fraction_saved:.4f}")
        print(f"Steps in bisection search: {search_steps}")
        break
    else:
        if amount > required_amount:
            fraction_saved_high = fraction_saved
        else:
            fraction_saved_low = fraction_saved
        fraction_saved = (fraction_saved_low + fraction_saved_high) / 2
