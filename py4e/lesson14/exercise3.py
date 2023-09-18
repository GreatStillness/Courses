import json
import urllib.parse
import urllib.request

serviceurl = 'http://py4e-data.dr-chuck.net/json?'

address = input('Enter location: ')
if len(address) < 1:
    print("Location is empty!")
    quit()

params = dict()
params['address'] = address
params['key'] = 42
url = serviceurl + urllib.parse.urlencode(params)

request = urllib.request.urlopen(url)
response_data = request.read().decode()
response_json = json.loads(response_data)


print(response_json["results"][0]["place_id"])
