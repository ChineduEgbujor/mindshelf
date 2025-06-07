import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import os, json

# Only initialize once
if not firebase_admin._apps:
    sa_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if not sa_json:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT environment variable not set")
    sa_info = json.loads(sa_json)
    cred = credentials.Certificate(sa_info)
    #cred = credentials.Certificate("app/moodmate-d9029-firebase-adminsdk-fbsvc-f71b42d0b6.json")
    firebase_admin.initialize_app(cred)

def verify_token(id_token: str):
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token['uid']
    except Exception as e:
        print(f"[Auth Error] {e}")
        return None
