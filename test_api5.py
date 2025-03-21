
import urllib.request
import urllib.parse

def get_data(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    return data

# Test export endpoint (CSV)
user_id = "cccccccc-cccc-cccc-cccc-cccccccccccc"
params = urllib.parse.urlencode({
    "user_id": user_id,
})
print("Testing CSV export endpoint...")
export_data = get_data(f"http://localhost:8000/api/v1/levels/export/csv?{params}")
csv_lines = export_data.split("\n")
print(f"Successfully exported {len(csv_lines) - 2} records to CSV") # -2 for header and empty last line
print(f"CSV header: {csv_lines[0]}")
print(f"First data row: {csv_lines[1]}")


