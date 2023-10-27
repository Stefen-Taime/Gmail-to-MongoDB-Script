import os
from urllib.parse import quote_plus
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pymongo.mongo_client import MongoClient
import schedule
import time
import pymongo

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def send_emails_to_mongodb():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        label_ids = ['CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL', 'CATEGORY_UPDATES', 'CATEGORY_FORUMS']
        client = pymongo.MongoClient("mongodb+srv://username:password*@host/admin?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)

        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        db = client['gmail_db']
        collection = db['emails']

        for label_id in label_ids:
            results = service.users().messages().list(userId='me', labelIds=label_id, maxResults=5).execute()
            messages = results.get('messages', [])
            if not messages:
                print(f'No messages found in {label_id}.')
            else:
                print(f'Messages in {label_id}:')
                for message in messages:
                    email_data = read_email(service, message['id'])
                    email_data['label'] = label_id
                    existing_message = collection.find_one({'message_id': email_data['message_id']})
                    if existing_message:
                        print(f'Message {email_data["message_id"]} already exists, skipping.')
                        continue  # Skip this message if it already exists in MongoDB
                    collection.insert_one(email_data)
                print('-' * 50)

    except Exception as error:
        print(f'An error occurred: {error}')

def read_email(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id, format='metadata').execute()
    headers = message['payload']['headers']
    email_data = {
        'message_id': message_id,
        'from': next((header['value'] for header in headers if header['name'].lower() == 'from'), 'No Sender'),
        'subject': next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject'),
        'snippet': message.get('snippet', 'No Snippet'),
        'date': next((header['value'] for header in headers if header['name'].lower() == 'date'), 'No Date')
    }
    print(email_data['subject'])
    return email_data

if __name__ == '__main__':
    schedule.every(1).minutes.do(send_emails_to_mongodb)
    print("Script is running. Emails will be sent to MongoDB every minute.")
    while True:
        schedule.run_pending()
        time.sleep(1)
