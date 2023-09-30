annual_salary = float(input("Enter your annual salary: "))
percent_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_rise = float(input("Enter the semi-annual raise, as a decimal: "))
portion_saved = annual_salary / 12 * percent_saved
portion_down_payment = 0.25
current_savings = 0
r = 0.04
months = 0
while current_savings < total_cost * portion_down_payment:
    current_savings += current_savings * r / 12 + portion_saved
    months += 1
    if months % 6 == 0:
        annual_salary *= 1 + semi_annual_rise
        portion_saved = annual_salary / 12 * percent_saved
print(f"Number of months: {months}")
