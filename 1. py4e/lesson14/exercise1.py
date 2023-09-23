import urllib.request
import xml.etree.ElementTree as ElementTree

address = input('Enter location: ')
if len(address) < 1:
    print("Address is not defined!")
    quit()

request = urllib.request.urlopen(address)

data = request.read()
tree = ElementTree.fromstring(data)

comments = tree.findall('comments/comment')
count = 0
for comment in comments:
    count += int(comment.find("count").text)
print(count)