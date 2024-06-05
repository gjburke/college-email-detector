import pickle
from load_emails import load_emails
from process_emails import process_emails
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import metrics

def main():
    # load emails
    college_emails = load_emails("../training_data/college")
    regular_emails = load_emails("../training_data/regular")
    print("loaded {} {}", len(college_emails), len(regular_emails))
    # process them (index then vectorize), cut so they're equal size
    college_emails = process_emails(college_emails)
    regular_emails = process_emails(regular_emails)
    max_amount = min(len(college_emails), len(regular_emails))
    college_emails = college_emails[:max_amount]
    regular_emails = regular_emails[:max_amount]
    print("processed")
    # combine emails into corresponding x with y labels
    X = college_emails + regular_emails
    y = [1] * max_amount + [0] * max_amount
    # split testing data, train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=59)
    print("split-------------------------------------------------------")
    print("X_train: {}\nY_train: {}", X_train, y_train)
    print("X_test: {}\nY_test: {}", X_test, y_test)
    print("onto training-----------------------------------------------")
    model = svm.SVC()
    model.fit(X_train, y_train)
    print("model has fit")
    y_pred = model.predict(X_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    # saving the model
    with open("../model.pkl", "wb") as f:
        pickle.dump(model, f)
    # to load the file:
    #with open("../model.pkl","rb") as f:
    #model = pickle.load(f)



if __name__ == "__main__":
  main()