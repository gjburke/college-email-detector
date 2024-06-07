import pickle
from email_interaction import get_emails
from email_interaction import label_emails
from process_emails import process_emails

def main():
    # get emails, process them
    ids, emails = get_emails(200)
    processed_emails = process_emails(emails)
    # load the model
    with open("../model.pkl","rb") as f:
        model = pickle.load(f)
    # predict with model
    predictions = model.predict(processed_emails)
    # output results
    for i in range(0, len(emails), 1):
        match predictions[i]:
            case 0:
                print("Not a college email")
            case 1:
                print("A college email")
            case _:
                print("Something went wrong")
        print("Email id: " + str(ids[i]) + " - " + str(emails[i][:100]))
    # label as college email based on output
    print(predictions)
    print(ids)
    label_emails(predictions, ids, "test-college-email")

if __name__ == "__main__":
    main()