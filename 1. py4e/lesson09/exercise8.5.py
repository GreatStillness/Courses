file_name = input("Enter a file name: ")
try:
    file_handle = open(file_name, "r")
except:
    print("The problem while opening the file:", file_name)
    quit()

count = 0

for string in file_handle:
    if string.startswith("From "):
        print(string.split()[1])
        count = count + 1

print("There were", count, "lines in the file with From as the first word")
