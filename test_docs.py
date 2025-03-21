
import urllib.request

def get_data(url):
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    return data

# Check if Swagger UI is available
try:
    swagger_data = get_data("http://localhost:8000/docs")
    if "Swagger UI" in swagger_data:
        print("Swagger UI is available at: http://localhost:8000/docs")
    else:
        print("Swagger UI response received but unexpected content")
except Exception as e:
    print("Error accessing Swagger UI:", e)


