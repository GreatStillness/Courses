def computepay(h, r):
    if h > 40:
        return r * (40 + (h - 40) * 1.5)
    else:
        return h * r


hours = float(input("Enter Hours:"))
rate = float(input("Enter Rate:"))
p = computepay(hours, rate)
print("Pay", p)
