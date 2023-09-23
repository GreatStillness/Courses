import re

filehandle = open("regex_sum_1818493.txt")
numbers = list()

for string in filehandle:
    matches = re.findall("\\d+", string)
    if len(matches) < 1:
        continue
    for match in matches:
        numbers.append(int(match))

print(sum(numbers))
