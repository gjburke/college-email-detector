"""Module providing a way to load emails from a given directory"""

import os

def load_emails(directory):
    emails = []
    for filename in os.listdir(directory):
        # filePath is a string of the specific file directory
        file_path = os.path.join(directory, filename)
        if (os.path.isfile(file_path)):
			# reads file by file and saves the array to data list
            f = open(file_path, "r")
            email = f.readlines()
            email = [sub[:-1] for sub in email]
            f.close()
            emails.append(email)
    return emails