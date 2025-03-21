
import urllib.request
import json

def get_json(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    return json.loads(data)

# Test health endpoint
print("Health:", get_json("http://localhost:8000/health"))

# Test levels endpoint for a user
user_id = "cccccccc-cccc-cccc-cccc-cccccccccccc"
try:
    print("Levels:", get_json(f"http://localhost:8000/api/v1/levels/?user_id={user_id}&page=1&page_size=5"))
except Exception as e:
    print("Error:", e)

