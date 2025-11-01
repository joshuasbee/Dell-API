import requests
from datetime import datetime
import json
from api_keys import CLIENT_ID
from api_keys import CLIENT_SECRET

# Get the authorization token using the API key
auth_url = "https://apigtwb2c.us.dell.com/auth/oauth/v2/token"
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}
auth_response = requests.post(auth_url, data=auth_data)
access_token = auth_response.json().get('access_token')

# Get the warranty information about one item passed in with the token
def fetch_warranty(service_tag, token):
    url = f"https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5/asset-entitlements?servicetags={service_tag}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    try:
        return response.json()
    except Exception as e:
        return {"error": f"Failed to parse JSON: {e}", "raw": response.text}

# Testing area

# response = fetch_warranty('', access_token)

# print(json.dumps(response, indent=2))

# filtered = []
# for item in response:
#     entitlements = item.get('entitlements', [])
#     latest_end = None

#     if entitlements:
#         # Convert endDate strings to datetime objects and find the latest
#         latest_end = max(
#             (datetime.fromisoformat(e['endDate'].replace('Z', '')) for e in entitlements if 'endDate' in e),
#             default=None
#         )

#     filtered.append({
#         'serviceTag': item.get('serviceTag'),
#         'productLineDescription': item.get('productLineDescription'),
#         'Warranty End': latest_end.strftime('%Y-%m-%d') if latest_end else None
#     })

# print(filtered)
