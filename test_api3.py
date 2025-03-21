
import urllib.request
import json
import urllib.parse

def get_json(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    return json.loads(data)

# Test filtering by date
user_id = "cccccccc-cccc-cccc-cccc-cccccccccccc"
start_date = "2021-02-15T00:00:00"
stop_date = "2021-02-16T00:00:00"
params = urllib.parse.urlencode({
    "user_id": user_id,
    "start": start_date,
    "stop": stop_date,
    "page": 1,
    "page_size": 5
})
print("Filtered by date range:", start_date, "to", stop_date)
filtered_results = get_json(f"http://localhost:8000/api/v1/levels/?{params}")
print("Total entries in range:", filtered_results["total"])
print("First entries:")
for item in filtered_results["items"]:
    print("  " + item["timestamp"] + ": " + str(item["glucose_value"]) + " mg/dL")


