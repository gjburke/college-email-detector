import os

# accessing the dictionary
d = open("../dictionary.txt", "r")
dictionary = d.readlines()
dictionary = [sub[:-1] for sub in dictionary]

def index_email(email):
    # indexing based on dictionary
    indices = []
    for word in email:
        if word in dictionary:
            indices.append(dictionary.index(word))
    return indices

def vectorize_email(indices):
    # create vector with ones at corresponding dictionary point
    vector = [0] * len(dictionary)
    for index in indices:
        vector[index] = 1
    return vector

def process_emails(emails):
    print("Processing... {}", len(emails))
    processed_emails = []
    for email in emails:
        indexed_email = index_email(email)
        vectorized_email = vectorize_email(indexed_email)
        processed_emails.append(vectorized_email)
    print("processed {}", len(processed_emails))
    return processed_emails