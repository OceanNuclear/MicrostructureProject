#!C:\Users\Ocean\AppData\Local\Programs\Python\Python36-32\python.exe
import numpy as np
import matplotlib.pyplot as plt

#Choose temperature to plot for,
#Report no. of lines.
#Read file: store variables,
#Plot with stored variable
#Show plot

T = str(input("Temperature?"))
#fileName = ["fast", "slow", "prev fast", "prev slow"]
#fileName = ["fast", "slow"]
fileName = ["slow"]
for n in range (len(fileName)):
	fileName[n] = str(fileName[n])+ "_"+ T+ "C.txt"


Stress = ["",]*len(fileName)
Strain = ["",]*len(fileName)
inFile = ["",]*len(fileName)

for speed in range (len(fileName)):
	inFile = fileName[speed]
#1: Report no. of lines
	numLines = sum(1 for line in open(inFile))
	print(inFile, "has", numLines,"data points.")
	Stress[speed] = np.zeros(numLines)
	Strain[speed] = np.zeros(numLines)

#2: Open again to read variables
	f = open(inFile, "r")
	f.seek(0)	#cause I'm paranoid and pedantic
	for n in range (numLines):
		Data = f.readline()
		Strain[speed][n] = Data.split()[0]
		Stress[speed][n] = Data.split()[1]
	t = str(fileName[speed])
	plt.plot(Strain[speed], Stress[speed], label = t, marker= '.')


plt.legend()
plt.legend(loc="lower right")#, bbox_to_anchor=(1,1))
plt.title(str(T)+ r'$\degree$'+ "C")
plt.xlabel(r'$\varepsilon$')
plt.ylabel(r'$\sigma$')
plt.ylim(bottom = 0)
plt.show()
