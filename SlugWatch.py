import firebase_admin
import numpy as numpy
import datetime
import matplotlib.pyplot as plt
import random
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('C:/Users/Ryan/Documents/VSCode/.venv/ServiceAccountKey.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

class GymCheckIn:
    timeOfCheckIn = 0 #time of check in
    
    def __init__(self):
            self.timeOfCheckIn = datetime.datetime.now().isoformat()

GymCheckIns = []

#Code neo found online
def categorize_timestamps_by_hour(timestamps):

    hour_counts = {}
    for i in range(24):
        hour_counts[i] = 0
    for timestamp in timestamps:
        hour = datetime.datetime.fromisoformat(timestamp).hour
        if hour not in hour_counts:
            hour_counts[hour] = 0
        hour_counts[hour] += 1
    return hour_counts

# Somehow a new gymcheckin must be registered
# Ideally this would be received from the school
for i in range(9):
    GymCheckIns.append(GymCheckIn())


# This loop creates a document for each gymcheckin containing the timestamp of the checkin
GymGoerNumber = 1
for i in GymCheckIns:
    timeString = str(i.timeOfCheckIn)
    numberString = str(GymGoerNumber)
    UserString = "Gym Goer:" + str(GymGoerNumber)
    doc_user = db.collection("Check-in Time Stamps").document(UserString)
    doc_user.set({"Time of Check In": timeString }, merge=False)
    GymGoerNumber += 1


arrayOfTimes = []
for goer in GymCheckIns:
    arrayOfTimes.append(goer.timeOfCheckIn)

hourArray = categorize_timestamps_by_hour(arrayOfTimes)
for i in range(24):
    doc_hour = db.collection("Number of Goers each Hour").document("AllHours")
    doc_hour.set({"Hour" + str(i)+ ":": hourArray[i] }, merge=True)