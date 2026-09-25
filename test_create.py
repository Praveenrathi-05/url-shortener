import requests

response = requests.post("http://127.0.0.1:5000/create", json={"url": "https://example.com/page?id=5"})
print(response.text)