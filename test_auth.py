import requests
import json

# Test login endpoint
print("=" * 50)
print("Testing Authentication API")
print("=" * 50)

url = "http://127.0.0.1:8000/api/auth/login/"
data = {
    "username": "admin",
    "password": "admin123"
}

print(f"\nSending POST request to: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("\n" + "=" * 50)

try:
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print("\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Authentication is working!")
        user_data = response.json().get('user', {})
        print(f"\nLogged in as: {user_data.get('username')}")
        print(f"Is Admin: {user_data.get('is_admin')}")
        print(f"Is Superadmin: {user_data.get('is_superadmin')}")
    else:
        print("\n❌ FAILED! Authentication not working")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 50)
