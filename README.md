# Gmail to MongoDB Script

## Description

This script facilitates the automation of fetching emails from a user's Gmail account and storing them into a MongoDB database. The emails fetched are filtered by specific labels such as Promotions, Social, Updates, and Forums. The script is intended to run continuously, checking for new emails every minute.

## Dependencies

- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`
- `pymongo`
- `schedule`

You can install the necessary dependencies via pip:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pymongo schedule


Setup
Create a project on the Google Cloud Platform Console.
Enable the Gmail API for your project.
Download the client configuration file credentials.json and place it in the root directory of this script.
Setup a MongoDB Atlas cluster and obtain the connection string.
Configuration
Set up your Gmail API credentials and save them as credentials.json in the script directory.
Update the MongoDB connection string in the MongoClient instantiation within the send_emails_to_mongodb function.
Usage
Run the script from the command line:

bash
Copy code
python script_name.py
Replace script_name.py with the name you saved the script as.

The script will prompt you to authorize access to your Gmail account upon the first run. Follow the on-screen instructions to complete the authorization. Once authorized, a token.json file will be created which will be used for subsequent authorizations.

The script will run indefinitely, checking for new emails every minute and storing them into the specified MongoDB database and collection. Each email entry in the database will contain the message id, sender, subject, snippet, date, and label.

Functions
send_emails_to_mongodb(): Main function to authenticate, connect to Gmail and MongoDB, fetch emails, and store them into the database.
read_email(service, message_id): Helper function to parse the email metadata.
Scheduling
The script uses the schedule library to run the send_emails_to_mongodb function every minute. This interval can be adjusted by modifying the following line:

python
Copy code
schedule.every(1).minutes.do(send_emails_to_mongodb)
Error Handling
Basic error handling is provided through try-except blocks. Any errors that occur during the execution will be printed to the console.

vbnet
Copy code

Now, you can upload this README file to your GitHub repository to provide the 
