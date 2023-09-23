file_name = input("Enter a file name: ")
try:
    file_handle = open(file_name, "r")
except:
    print("The problem while opening the file:", file_name)
    quit()

count = 0
total = 0
for string in file_handle:
    if string.startswith("X-DSPAM-Confidence:"):
        count = count + 1
        total = total + float(string[(string.find(":") + 1):])
print("Average spam confidence:", total / count)
