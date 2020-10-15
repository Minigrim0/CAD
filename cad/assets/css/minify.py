import requests

url = 'https://cssminifier.com/raw'
data = {'input': open('cad.css', 'rb').read()}
response = requests.post(url, data=data)

print(response.text)
