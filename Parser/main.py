# from fileinput import filename
# from posixpath import dirname
import requests
import json
import os

state = 'FL'
headers = {
    'accept': 'application/geo+json',
    'User-Agent': 'application in Python; email, if you need: dima-ano0@yandex.ru',
}
params = (
    ('state', state),
)

response = requests.get('https://api.weather.gov/stations', headers=headers, params=params)
print(response.status_code)

rewrite_flag = False
if (response.status_code == 200) and (rewrite_flag == True):

    dirname = 'utils'
    filename = 'data_stations_file.json'
    dirpath = os.path.join(os.getcwd(), dirname)
    filename = os.path.join(dirpath, filename)
    
    with open(filename, "w") as write_file:
        json.dump(response.json(), write_file)
        print('data_file has been overwritten')

