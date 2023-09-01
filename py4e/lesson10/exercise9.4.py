filename = input("Enter file: ")
if len(filename) < 1:
    name = "mbox-short.txt"

try:
    filehandle = open(filename)
except:
    print("Problem while opening the file", filename)
    exit()

emailsCount = dict()
for string in filehandle:
    if string.startswith("From "):
        email = string.split()[1]
        emailsCount[email] = emailsCount.get(email, 0) + 1

biggestCount = None
biggestCountMail = None

for mail, count in emailsCount.items():
    if biggestCount is None or biggestCount < count:
        biggestCount = count
        biggestCountMail = mail

print(biggestCountMail, biggestCount)
