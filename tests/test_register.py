import requests

url = 'http://localhost:5000/register'

# Define the JSON data for a new user
user_data = {
    'username': 'testuser',
    'email': 'testuser@example.com',
    'password': 'testpassword'
}

response = requests.post(url, json=user_data)

if response.status_code == 200:
    print('User logedin successfully:', response.json())
elif response.status_code == 400:
    print('Bad request:', response.json())
elif response.status_code == 500:
    print('Internal server error:', response.json())
else:
    print(f'Unexpected status code: {response.status_code}')

print('Response text:', response.text)