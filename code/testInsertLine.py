import requests


url = 'http://localhost:5000/insertToken'

# Define the data you want to send (the token)
payload = {
    'token': 'your_token_value_here'
}

# Send the POST request to insert the token
try:
    response = requests.post(url, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error occurred: {e}")