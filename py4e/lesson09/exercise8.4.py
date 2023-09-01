filename = input("Enter file: ")

try:
    file_handle = open(filename)
except:
    print("Problem while opening file", filename)
    quit()

words = list()
for string in file_handle:
    for word in string.split():
        if word not in words:
            words.append(word)

words.sort()
print(words)