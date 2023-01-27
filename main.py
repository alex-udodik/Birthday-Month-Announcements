import os

from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

def getNextMonth():
    currentMonth = datetime.now().month

    if currentMonth == 12:
        currentMonth = 1
    else:
        currentMonth += 1

    return currentMonth


load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_URL = os.getenv('MONGO_URL')

client = MongoClient("mongodb+srv://"+MONGO_USER+":" + MONGO_PASSWORD + "@" + MONGO_URL + "/?retryWrites=true&w=majority")
db = client.FUPC
book = db.Members

members = book.find()

targetMonth = getNextMonth()

birthdaysForTargetMonth = []

for x in members:
    month = x["Birthdate"].month
    if month == targetMonth:
        birthdaysForTargetMonth.append(x)

sortedNamesByDay = sorted(birthdaysForTargetMonth, key=lambda i: i["Birthdate"].day)

names = []

for x in sortedNamesByDay:
    names.append(x["Name"])

print(names)