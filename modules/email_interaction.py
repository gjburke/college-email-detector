from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import base64
import re
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
nltk.download('punkt')

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.modify"]

# Takes in number of emails to scan, outputs a list of [ids, emails] which have a body and stems all the words
# and separates each email into a list of words
def get_emails(num_emails):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("../token.json"):
    creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "../credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("../token.json", "w") as token:
      token.write(creds.to_json())

  # Create list of all the emails and their 
  emails = []
  ids = []

  try:
    # Call the Gmail API and get messages
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=num_emails).execute()
    email_ids = results.get('messages', [])

    # For now, print the messages
    for email_id in email_ids:
      try:
        email = service.users().messages().get(userId="me", id=email_id['id'], format='full').execute()

        # Get body or snippet
        raw_body = email.get("snippet")
        if email.get("payload").get("body").get("data"):
          decoded_data = base64.urlsafe_b64decode(email.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
          raw_body = str(BeautifulSoup(decoded_data, "lxml").body())

        ids.append(email_id['id'])
  
        # Cleaning up everything 
        body = raw_body.lower()

        # Normalizing URLS: replaced with "httpaddr"
        body = re.sub(r"(http|https)://[a-z0-9.\-/_]+(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", " httpaddr ", body)

        # Normalizing Email Addresses: replaced with "emailaddr"
        body = re.sub(r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", " emailaddr ", body)

        # Take out html, css
        body = re.sub(r"<.*?>", " ", body)
        body = re.sub(r"{.*?}", " ", body)
        body = re.sub(r"\.\w+(?:-\d+)?", " ", body)
        body = re.sub(r"#\w+(?:-\d+)?", " ", body)

        # Normalizing Numbers: replced with "number"
        body = re.sub(r"[0-9]+", " number ", body)

        # Normalizing Dollars: replaced with "dollar"
        body = re.sub(r"$", " dollar ", body)

        # Removal of Non-Words
        body = re.sub(r"[@\$/#\.:&*\+=\[\]\?!\(\)\{\},\'\">_<;%\^\\\|]","", body)
        body = re.sub(r"-", " ", body)
        body = re.sub(r"\s+", " ", body, flags = re.MULTILINE)

        # Tokenize and stem words
        words = nltk.word_tokenize(body)
        ps = PorterStemmer()
        i = 0
        while i < len(words):
          try:
            words[i] = ps.stem(words[i])
          except:
            words[i] = ""
          i += 1
        words = list(filter(None, words))
        emails.append(words)
      except Exception as error:
        print(error)
      
  except HttpError as error:
    # Handle errors from gmail API.
    print(f"An error occurred: {error}")

  return [ids, emails]

def label_emails(predictions, ids, label_name):
  if len(predictions) != len(ids):
    print("Labels and ids don't match")
    return
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("../token.json"):
    creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "../credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("../token.json", "w") as token:
      token.write(creds.to_json())
  # Change the emails tag_name based on the label
  try:
    # Call the Gmail API and get messages
    service = build("gmail", "v1", credentials=creds)
    # Create the label to use if not already present
    new_label = {
      'name': label_name,
      'messageListVisibility': 'show',
      'labelListVisibility': 'labelShow',
    } 
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    contains = False
    for label in labels:
      if label['name'] == label_name:
        contains = True
    if not contains:
      service.users().labels().create(userId='me', body=new_label).execute()
    # Get the label id as to add it
    label_id = ""
    for label in labels:
      if label['name'] == label_name:
        label_id = label['id']
    # Iterate over all the emails ids
    print("label_id = " + str(label_id))
    for i in range(0, len(predictions), 1):
      print(predictions[i])
      if predictions[i] == 1:
        print("Adding label")
        service.users().messages().modify(userId='me', id=ids[i], body={'addLabelIds': [label_id]}).execute()
  except HttpError as error:
    # Handle errors from gmail API.
    print(f"An error occurred: {error}")

#if __name__ == "__main__":
#  print(get_emails(5))