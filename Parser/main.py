from fileinput import filename
from posixpath import dirname
import requests
import json
import os


headers = {
    'accept': 'application/geo+json',
}
params = (
    ('state', 'FL'),
)

response = requests.get('https://api.weather.gov/stations', headers=headers, params=params)
print(response.status_code)

rewrite = True
if (response.status_code == 200) and (rewrite == True):

    dirname = 'utils'
    filename = 'data_stations_file.json'
    dirpath = os.path.join(os.getcwd(), dirname)
    filename = os.path.join(dirpath, filename)
    
    with open(filename, "w") as write_file:
        json.dump(response.json(), write_file)
        print('data_file has been overwritten')