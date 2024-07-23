import requests

url = 'http://127.0.0.1:8086/query?db=abschluss_pi&q=select * from umwelt'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)