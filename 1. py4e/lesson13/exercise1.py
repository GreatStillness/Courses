# Exercise: Scraping HTML Data with BeautifulSoup
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

url = "http://py4e-data.dr-chuck.net/comments_1818495.html"
request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urlopen(request).read()
soup = BeautifulSoup(html, 'html.parser')

total = 0
count = 0
tags = soup('span')
for tag in tags:
    total += int(tag.contents[0])
    count += 1
print("Count", count)
print("Sum", total)
