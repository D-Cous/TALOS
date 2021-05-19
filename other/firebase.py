import other.creds as creds
import pyrebase


config = {
  'apiKey': "",
  'authDomain': "",
  'databaseURL': "",
  'projectId': "",
  'storageBucket': "",
  'messagingSenderId': "",
  'appId': "",
  'serviceAccount': creds.firebaseServiceAccount
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

