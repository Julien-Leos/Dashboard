import pyrebase

config = {
    "apiKey": "AIzaSyBTjwyIi20T5CKnXJryAe5aJ1U6u5CHkeY",
    "authDomain": "dashboard-5d0a1.firebaseapp.com",
    "databaseURL": "https://dashboard-5d0a1.firebaseio.com",
    "storageBucket": "dashboard-5d0a1.appspot.com"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()