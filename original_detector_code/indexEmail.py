import os

def indexEmail():

	#accessing the dictionary
	d = open("dictionary.txt", "r")
	dic = d.readlines()
	dic = [sub[:-1] for sub in dic]

	readDir = "regular-emails"
	writeDir = "regular-emails-indicies/email.txt"
	#iterating through each email file
	for filename in os.listdir(readDir):
		# filePath is a string of the specific file directory
		filePath = os.path.join(readDir, filename)
		if (os.path.isfile(filePath)):
			# reads file by file and saves the array to data list
			f = open(filePath, "r")
			data = f.readlines()
			data = [sub[:-1] for sub in data]
			f.close()
		# Creating an array for the indicies
		emailInd = []
		# Addign the indicies that match with each word of the email
		i = 0
		while i < len(data):
			word = data[i]
			j = 0
			while j < len(dic):
				if word == dic[j]:
					emailInd.append(j)
					break
				j += 1
			i += 1

		# Writing the email indicies to a file
		# Writing Tokenized Words to a Text Document
		path = uniquify(writeDir)
		file = open(path, "w")
		for ind in emailInd:
			strInd = str(ind)
			file.writelines(strInd + "\n")
		file.close()

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path

indexEmail()