from libsvm.svmutil import *
from sklearn.model_selection import train_test_split
import os
import numpy as np

def trainSVM():

	print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

	X = []
	y = []
	collegeData = []
	regularData = []

	# get data from files 
	collegeDir = "college-emails-vectorized"
	regDir = "regular-emails-vectorized"
	#iterating through college emails
	for filename in os.listdir(collegeDir):
		# filePath is a string of the specific file directory
		filePath = os.path.join(collegeDir, filename)
		if (os.path.isfile(filePath)):
			# reads file by file and saves the array to data list
			f = open(filePath, "r")
			collegeData = []
			for line in f:
				collegeData.append(int(line[:-1]))
			f.close()
		X.append(collegeData)
		y.append(1)
	# iterating through regular emails 
	for filename in os.listdir(regDir):
		# filePath is a string of the specific file directory
		filePath = os.path.join(collegeDir, filename)
		if (os.path.isfile(filePath)):
			# reads file by file and saves the array to data list
			f = open(filePath, "r")
			regularData = []
			for line in f:
				regularData.append(int(line[:-1]))
			f.close()
		X.append(regularData)
		y.append(0)

	print()

	# svm
	# splittig data randomly
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=59)

	# problem?
	prob = svm_problem(y_train, X_train)

	#exp = -15 
	#while exp < 15:
	#	c = 2**exp

	#	print("C: ", c)
		# parameters
	param = svm_parameter('-t 0')

		# train
	model = svm_train(prob, param)

		# predict
	p_labs, p_acc, p_vals = svm_predict(y_test, X_test, model)

	print("------------------------------------------------------------------")
	#	exp += 1

	zeros = 0
	ones = 0

	for y in y_test:
		if y == 0:
			zeros += 1
		if y == 1:
			ones += 1

	print("Percent of Ones: ", (ones / (zeros + ones)))

# defining gaussian kernel
#def gaussianKernel(x1, x2, sigma=0.1):
	
	#gram_matrix = np.zeros((X1.shape[0], X2.shape[0]))


trainSVM()