import requests

url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
response = requests.get(url)

with open('files/hubble.jpeg', 'wb') as file:
    file.write(response.content)