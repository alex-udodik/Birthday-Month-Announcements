import json
import os
import boto3

from botocore.exceptions import ClientError
from datetime import datetime
from pymongo import MongoClient
def getNextMonth():
    currentMonth = datetime.now().month

    if currentMonth == 12:
        currentMonth = 1
    else:
        currentMonth += 1

    return currentMonth

def getNextMonthName():
    currentMonth = datetime.now().month

    if currentMonth == 12:
        currentMonth = 1
    else:
        currentMonth += 1

    datetime_object = datetime.strptime(str(currentMonth), "%m")
    full_month_name = datetime_object.strftime("%B")
    return full_month_name

def sendEmail(names):
    monthName = getNextMonthName()
    
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "*** <>"
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = ""
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-west-2"
    
    # The subject line for the email.
    SUBJECT = "FUPC Members Birthdays for " + monthName
    
    para = ""
    for x in names:
        para += x
        para += "\n"
        
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("FUPC Members Birthdays for " + monthName + "\r\n\n" + para + "\n" + "This email was sent with Amazon SES using the AWS SDK for Python (Boto).")
                
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    
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
    
    names = []

    for x in sortedNamesByDay:
        names.append(x["Name"])
    
    sendEmail(names)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
