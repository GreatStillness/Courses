import json
import urllib.request

address = input('Enter location: ')
if len(address) < 1:
    print("Address is not defined!")
    quit()

request = urllib.request.urlopen(address)

data = request.read()

comments = json.loads(data)["comments"]

count = 0
for comment in comments:
    count += int(comment["count"])
print(count)
