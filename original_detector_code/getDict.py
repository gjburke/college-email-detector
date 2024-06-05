# WIP
# Meant to create dictionary of most common words pulled from all the emails in the email folder

import os
from collections import Counter

def getDict(): 

	allData = []
	numWordsInDict = 400
	wordCutOff = 14

	directory = "college-emails"
	for filename in os.listdir(directory):
		# filePath is a string of the specific file directory
		filePath = os.path.join(directory, filename)
		if (os.path.isfile(filePath)):
			# reads file by file and saves the array to data list
			f = open(filePath, "r")
			data = f.readlines()
			data = [sub[:-1] for sub in data]
			f.close()
			# adds data to allData lsit
			allData += data
	#print(allData)

	# finding the most common words in the master data
	counter = Counter(allData)
	mostOccur = counter.most_common(numWordsInDict)

	print("---------------------------------------------------------------------------------------------------")
	print(mostOccur)

	# creating final dictionary
	finalDict = []
	#i = 0
	#while mostOccur[i][1] >= wordCutOff:
	#	finalDict.append(mostOccur[i][0])
	#	i += 1

	i = 0 
	while i < len(mostOccur):
		finalDict.append(mostOccur[i][0])
		i += 1

	# ordering alphabetically
	finalDict = sorted(finalDict)

	print("---------------------------------------------------------------------------------------------------")
	print(finalDict)
	print(len(finalDict))

	d = open("dictionary.txt", "w")
	for t in finalDict:
		d.write(t + "\n")
	d.close()

getDict()