"""Module with a function to make a dicitonary from given emails"""

from collections import Counter
from load_emails import load_emails

def make_dict(emails):
    num_words = 400

    flattened_emails = []
    for email in emails:
        flattened_emails += email

    # Finding the most common words in the master data
    counter = Counter(flattened_emails)
    most_occur = counter.most_common(num_words)

    # Creating final dictionary
    dictionary = []

    for word in most_occur:
        dictionary.append(word[0])

    dictionary = sorted(dictionary)

    return dictionary[:num_words]

def save_dict(dictionary):
    d = open("../dictionary.txt", "w")
    for word in dictionary:
        d.write(word + "\n")
    d.close()


def main():
    emails = load_emails("../training_data/college")
    dictionary = make_dict(emails)
    save_dict(dictionary)


if __name__ == "__main__":
    main()
