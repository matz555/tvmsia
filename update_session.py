import requests

# Endpoint untuk pembaharuan sesi
SESSION_URL = "https://developers.broadpeak.io/api/session"
PAYLOAD = {
    "serviceId": "6c0958d82a830a02ca0936d9cfab8311",
    "category": "all"
}

def get_new_session():
    response = requests.post(SESSION_URL, json=PAYLOAD)
    if response.status_code == 200:
        session_data = response.json()
        return session_data["sessionid"]
    else:
        print("Error renewing session:", response.status_code)
        return None

new_session = get_new_session()
if new_session:
    print(f"New session ID: {new_session}")
