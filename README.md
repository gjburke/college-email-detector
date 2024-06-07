# college-email-detector

*Originally worked on from May 2020 – August 2022*

## Timeline of Creation

From May 2020 - August 2022: I was getting really annoyed at the amount of college emails I was getting Junior year, so I wanted to find a way to find them all quickly. I learned ML concepts through Stanford Coursera course. Then I gathered testing data, implemented SVM to classify data, achieved >95% accuracy.

From May 2024 - June 2024: Recreated code with present libraries, added functionality through user interaction so classification model can be applied to a user's inbox.

## Use

Clone repo to folder, setup virtual environment and install packages in requirements.txt

Go through Google's Gmail API quickstart for python in order to set up necessary credentials.

Run the program by navigating into the modules folder and running app.py, specify how many emails you want for it to scan and the label name for the detected college emails, log into your gmail to give access, and let it do its thing.

The program will scan and process the amount of emails specified, tagging an email if its a college promotional email or not. 

From there, you can do what you want with the emails (double check, delete, respond, etc)

## Additional Use

This could be used to classify a lot of different type of emails. There would just have to be manual data collection on the user's part. But once the emails are in the format of my testing data, it could work. Once thats complete, along with classification, it wouldn't be hard to change the code up a little to make it 'spam classifier' or something like that
