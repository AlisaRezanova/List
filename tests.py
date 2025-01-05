import requests

url = "http://127.0.0.1:8000/edit_title/2/"
headers = {"Content-Type": "application/json"}
data = {
    "note": "This is an updated note.",
    "rating": 8
}

response = requests.post(url, json=data, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")