#!C:\Users\Ocean\AppData\Local\Programs\Python\Python36-32\python.exe
import numpy as np
import glob
import os

#---------------------Make up file path---------------------------
def getFilePath(Temp, basePath):
	i = "t   "+str( '{:0=1.1E}'.format(Temp))
	filePaths = glob.glob(os.path.join( basePath ,'{0}*.txt'.format(i)))
	#if filePaths:
	#	print ("reading from", filePaths)
	return filePaths

#---------------------find the nearest five points' indices-------
def index(array, value):
	index = ( np.argsort(np.abs(array - value)) )[:5] #return the indices of the nearest 5 points.
	return index
