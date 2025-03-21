
import urllib.request
import json
import urllib.parse

def get_json(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {"raw_data": data[:100] + "..." if len(data) > 100 else data}

# Test export endpoint (JSON)
user_id = "cccccccc-cccc-cccc-cccc-cccccccccccc"
params = urllib.parse.urlencode({
    "user_id": user_id,
})
print("Testing JSON export endpoint...")
export_data = get_json(f"http://localhost:8000/api/v1/levels/export/json?{params}")
if isinstance(export_data, list):
    print(f"Successfully exported {len(export_data)} records to JSON")
    print(f"First record: {json.dumps(export_data[0], indent=2)[:150]}...")
else:
    print("Export data:", export_data)


