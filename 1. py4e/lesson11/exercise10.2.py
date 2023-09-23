filename = input("Enter file: ")
if len(filename) < 1:
    filename = "mbox-short.txt"

try:
    filehandle = open(filename)
except:
    print("Problem while opening the file", filename)
    exit()

hour_to_count = dict()
for string in filehandle:
    if string.startswith("From "):
        hour = string.split()[5].split(":")[0]
        hour_to_count[hour] = hour_to_count.get(hour, 0) + 1

hour_to_count = list(hour_to_count.items())
hour_to_count.sort()

for hour, count in hour_to_count:
    print(hour, count)
