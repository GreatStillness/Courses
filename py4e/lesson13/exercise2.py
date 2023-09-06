# Exercise: Following Links with BeautifulSoup
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

url = "http://py4e-data.dr-chuck.net/known_by_Mathilda.html"
print("Retrieving:", url)

count = 0
while count < 7:
    request = Request(url)
    html = urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    url = tags[17].get("href")
    print("Retrieving:", url)
    count += 1