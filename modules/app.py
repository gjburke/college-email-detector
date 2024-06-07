import pickle
from email_interaction import get_emails
from email_interaction import label_emails
from process_emails import process_emails

def main():
    # get number of emails and tag name from user
    print("Enter the amount of emails you want checked:", end=' ')
    num_emails = 0
    while True:
        try:
            num_emails = int(input())
            break
        except Exception as error:
            print("Must input a number. Error: " + str(error))
    print("Enter the name of the tag (reccomended - college-emails, college-promotional, etc):", end=' ')
    tag_name = ""
    while True:
        try:
            tag_name = str(input())
            break
        except Exception as error:
            print("Must use valid string. Error: " + str(error))
    # get emails, process them
    print("Fetching Emails...")
    ids, emails = get_emails(num_emails)
    print("Processing Emails...")
    processed_emails = process_emails(emails)
    # load the model
    print("Evaluating with Model...")
    with open("../model.pkl","rb") as f:
        model = pickle.load(f)
    # predict with model
    predictions = model.predict(processed_emails)
    # label as college email based on output
    print("Labelling...")
    label_emails(predictions, ids, tag_name)
    print("Done!")

if __name__ == "__main__":
    main()