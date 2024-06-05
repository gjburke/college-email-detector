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
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_emails(num_emails):
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
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

  # Create list of all the emails
  emails = []

  try:
    # Call the Gmail API and get messages
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=num_emails).execute()
    email_ids = results.get('messages', [])

    # For now, print the messages
    for email_id in email_ids:
      message = service.users().messages().get(userId="me", id=email_id['id'], format='full').execute()

      if message.get('payload').get('body').get('data'):
        # Get body
        decoded_data = base64.urlsafe_b64decode(message.get('payload').get('body').get('data').encode('ASCII').decode('utf-8'))
        raw_body = str(BeautifulSoup(decoded_data, "lxml").body())
  
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
      else:
        print(f"No body found for Email ID {email_id['id']}.")
      
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

  return emails

#if __name__ == "__main__":
#  print(get_emails(5))