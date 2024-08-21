import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    cred = credentials.Certificate("vicios-44d19-firebase-adminsdk-tm7ef-71f5ae5d66.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = initialize_firebase()
