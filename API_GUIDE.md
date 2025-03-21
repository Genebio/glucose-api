# Glucose API Usage Guide

This guide provides examples for using the deployed Glucose API.

## Live Demo

The API is deployed and available at:
- Documentation: https://glucose-api.onrender.com/docs
- Base URL: https://glucose-api.onrender.com

## Available User IDs

The demo is preloaded with glucose data for these users:
- `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa`
- `cccccccc-cccc-cccc-cccc-cccccccccccc`

## Example API Calls

### 1. Get Glucose Levels for a User

Retrieve glucose levels for a specific user:

```
GET /api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc
```

Complete URL:
```
https://glucose-api.onrender.com/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc
```

### 2. Filtering by Date Range

Filter readings between specific dates:

```
GET /api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc&start=2021-02-15T00:00:00&stop=2021-02-16T00:00:00
```

Complete URL:
```
https://glucose-api.onrender.com/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc&start=2021-02-15T00:00:00&stop=2021-02-16T00:00:00
```

### 3. Pagination and Sorting

Limit results to 10 per page and sort by glucose value:

```
GET /api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc&page=1&page_size=10&sort_by=glucose_value&sort_order=desc
```

Complete URL:
```
https://glucose-api.onrender.com/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc&page=1&page_size=10&sort_by=glucose_value&sort_order=desc
```

### 4. Get a Specific Glucose Level

Retrieve a specific glucose level by ID (you'll need to get an ID first from the list endpoint):

```
GET /api/v1/levels/{glucose_id}
```

Example:
```
https://glucose-api.onrender.com/api/v1/levels/12345678-1234-1234-1234-123456789abc
```
(Replace with an actual ID from your results)

### 5. Export Data

Export glucose levels to different formats:

```
GET /api/v1/levels/export/csv?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc
GET /api/v1/levels/export/json?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc
GET /api/v1/levels/export/excel?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc
```

## Using the API in Code

### Python Example

```python
import requests
import pandas as pd
from datetime import datetime, timedelta

# Define the base URL
base_url = "https://glucose-api.onrender.com"

# Get glucose levels for a specific time range
user_id = "cccccccc-cccc-cccc-cccc-cccccccccccc"
yesterday = (datetime.now() - timedelta(days=1)).isoformat()
today = datetime.now().isoformat()

# Make the API request
response = requests.get(
    f"{base_url}/api/v1/levels/",
    params={
        "user_id": user_id,
        "start": "2021-02-10T00:00:00",
        "stop": "2021-02-11T00:00:00",
        "page": 1,
        "page_size": 100
    }
)

# Process the response
if response.status_code == 200:
    data = response.json()
    print(f"Total records: {data['total']}")
    
    # Convert to pandas DataFrame for analysis
    df = pd.DataFrame([item for item in data["items"]])
    
    # Show average glucose value
    if not df.empty:
        print(f"Average glucose value: {df['glucose_value'].mean():.2f} mg/dL")
        print(f"Max glucose value: {df['glucose_value'].max():.2f} mg/dL")
        print(f"Min glucose value: {df['glucose_value'].min():.2f} mg/dL")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### JavaScript/TypeScript Example

```javascript
// Example using fetch API
async function getGlucoseLevels(userId, startDate, endDate) {
  const url = new URL('https://glucose-api.onrender.com/api/v1/levels/');
  
  // Add query parameters
  url.searchParams.append('user_id', userId);
  if (startDate) url.searchParams.append('start', startDate);
  if (endDate) url.searchParams.append('stop', endDate);
  url.searchParams.append('page', '1');
  url.searchParams.append('page_size', '100');
  
  try {
    const response = await fetch(url.toString());
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching glucose levels:', error);
    return null;
  }
}

// Usage
const userId = 'cccccccc-cccc-cccc-cccc-cccccccccccc';
getGlucoseLevels(userId, '2021-02-15T00:00:00', '2021-02-16T00:00:00')
  .then(data => {
    if (data) {
      console.log(`Total records: ${data.total}`);
      
      // Calculate statistics
      if (data.items.length > 0) {
        const values = data.items.map(item => item.glucose_value);
        const average = values.reduce((sum, val) => sum + val, 0) / values.length;
        const max = Math.max(...values);
        const min = Math.min(...values);
        
        console.log(`Average glucose value: ${average.toFixed(2)} mg/dL`);
        console.log(`Max glucose value: ${max.toFixed(2)} mg/dL`);
        console.log(`Min glucose value: ${min.toFixed(2)} mg/dL`);
      }
    }
  });
```