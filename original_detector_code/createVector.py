import os

def vectorizeEmail():

	#accessing the dictionary
	d = open("dictionary.txt", "r")
	dic = d.readlines()
	dic = [sub[:-1] for sub in dic]

	readDir = "regular-emails-indicies"
	writeDir = "regular-emails-vectorized/email.txt"
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

		# create vector that'll ultiamtely be used in machine learning
		vectorizedEmail = [0] * len(dic)
		i = 0
		while i < len(data):
			index = int(data[i])
			vectorizedEmail[index] = 1
			i += 1

		# writing vectors to text file
		path = uniquify(writeDir)
		file = open(path, "w")
		for ind in vectorizedEmail:
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

vectorizeEmail()