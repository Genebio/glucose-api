
import urllib.request
import json

def get_json(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    return json.loads(data)

# Get a specific glucose level
user_id = "cccccccc-cccc-cccc-cccc-cccccccccccc"
levels = get_json(f"http://localhost:8000/api/v1/levels/?user_id={user_id}&page=1&page_size=1")
if "items" in levels and len(levels["items"]) > 0:
    glucose_id = levels["items"][0]["id"]
    print("Single glucose level:", get_json(f"http://localhost:8000/api/v1/levels/{glucose_id}"))
else:
    print("No glucose levels found")


