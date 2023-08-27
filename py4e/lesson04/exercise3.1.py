hours = float(input("Enter Hours: "))
rate = float(input("Enter Rate: "))

if hours > 40:
    pay = rate * (40 + (hours - 40) * 1.5)
else:
    pay = hours * rate

print(pay)