import requests

r = requests.get('http://192.168.99.101/api/v1/commands/?cmd=volume&volume=80')

print(r.status_code)
