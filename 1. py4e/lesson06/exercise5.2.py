maximum = None
minimum = None
while True:
    value = input("Enter a number: ")

    if value == "done":
        break

    try:
        number = int(value)
    except:
        print("Invalid input")
        continue

    if minimum is None or minimum > number:
        minimum = number
    if maximum is None or maximum < number:
        maximum = number

print("Maximum is", maximum)
print("Minimum is", minimum)
