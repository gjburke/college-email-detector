# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def getEmails():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):
  
        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
  
    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
  
        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
  
    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
  
    # request a list of all the messages
    result = service.users().messages().list(userId='me', q='label:not-college-2', includeSpamTrash='True').execute()
  
    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
  
    # messages is a list of dictionaries where each dictionary contains a message id.
    
    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

  
            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)
  
            # Now, the data obtained is in lxml. So, we will parse 
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data , "lxml")
            body = soup.body()

            # Cleaning up the body by taking away unwanted html and other characters
            newBody = str(body)
            #print(newBody)
            #print("\n---------------------------------------------------------------------------------------\n")

            # Lower-Casing
            newBody = newBody.lower()

            # Taking out html tags
            #i = 0;
            #while i < len(newBody):
                #if newBody[i] == "<":
                    #start = i 
                    #j = start
                    #while newBody[j] != ">":
                        #j += 1
                    #end = j 
                    #newBody = newBody[0:start] + newBody[end + 1:]
                    #i -= 1
                #i += 1

            newBody = re.sub("<.*?>", "", newBody)

            # Normalizing URLS: replaced with "httpaddr"
            newBody = re.sub("(http|https)://[a-z0-9.\-/_]+", "httpaddr", newBody)

            # Normalizing Email Addresses: replaced with "emailaddr"
            newBody = re.sub("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", "emailaddr", newBody)

            # Normalizing Numbers: replced with "number"
            newBody = re.sub("[0-9]+", "number", newBody)

            # Normalizing Dollars: replaced with "dollar"
            newBody = re.sub("$", "dollar", newBody)

            #Removal of Non-Words
            newBody = re.sub("[@\$/#\.:&*\+=\[\]\?!\(\)\{\},\'\">_<;%\^\\\|]","", newBody)
            newBody = re.sub("-", " ", newBody)
            newBody = re.sub("\s+", " ", newBody, flags = re.MULTILINE)

            # Tokenization
            newWords = word_tokenize(newBody)

            # Word Stemming 
            ps = PorterStemmer()
            i = 0
            while i < len(newWords):
                try:
                    newWords[i] = ps.stem(newWords[i])
                except:
                    newWords[i] = ""
                i += 1

            # Printing Final Product
            #print(newBody)
            #print("\n---------------------------------------------------------------------------------------\n")
            #print(newWords)

            # Writing Tokenized Words to a Text Document
            path = uniquify("buffer-folder/email.txt")
            file = open(path, "w")
            for word in newWords:
                file.write(word + "\n")
            file.close()

        except:
            pass

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

getEmails()