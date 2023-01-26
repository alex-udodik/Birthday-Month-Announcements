import json
import os

from datetime import datetime
from pymongo import MongoClient

def getNextMonth():
    currentMonth = datetime.now().month

    if currentMonth == 12:
        currentMonth = 1
    else:
        currentMonth += 1

    return currentMonth
    
    
def lambda_handler(event, context):
    
    client = MongoClient("mongodb+srv://" + os.environ.get('MONGO_USER')+ ":" + os.environ.get('MONGO_PASSWORD') + "@" + os.environ.get('MONGO_URL') + "/test")
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
    print(sortedNamesByDay)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
