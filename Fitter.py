#!C:\Users\Ocea	n\AppData\Local\Programs\Python\Python36-32\python.exe
#This version plots a single Temperature only

import numpy as np
import matplotlib.pyplot as plt
import platform
import numpy as np
import header as h
#remember that h.index is to find the indices of the five nearest points.

#This program finds the data file of two temperatures,
#and spits out the residual for each (interpolated/averaged) point.	

def Residual( Temp , speed , folder ):
	filePathSim = folder+"Sim"+str(Temp)+"C_"+speed+".txt"
	#fileName = ["fast", "slow", "prev fast", "prev slow"]
	fileName = ["experimental/"+speed+"_"+str(Temp)+"C.txt", filePathSim]

	#---------------------------Experimental-------------------------
	inFile = fileName[0]
	#1: Report no. of lines
	numLines = sum(1 for line in open(inFile))
	#print("Experiment", str(Temp),"C", "has", numLines," data points")
	Stress_exp = np.zeros(numLines)
	Strain_exp = np.zeros(numLines)
	#2: Open again to read variables
	f = open(inFile, "r")
	for n in range (numLines):
		Data = f.readline()
		Strain_exp[n] = Data.split()[0]
		Stress_exp[n] = Data.split()[1]
	exp_max = max(Strain_exp); #print("Maximum extension in the experiment =", exp_max)
	f.close()
	#---------------------------Simulated-----------------------------
	inFile = fileName[1]
	#1: Report no. of lines
	numLines = sum(1 for line in open(inFile))
	#print("Simulated", str(Temp),"C", "has", numLines," data points")
	Stress_sim = np.zeros(numLines)
	Strain_sim = np.zeros(numLines)
	#2: Open again to read variables
	f = open(inFile, "r")
	for n in range (numLines):
		Data = f.readline()
		Strain_sim[n] = Data.split()[0]
		Stress_sim[n] = Data.split()[1]
	sim_max = max(Strain_sim); #print("Maximum extension in the experiment =", exp_max)
	f.close()

	#-------------------------Plot to find the maximum--------------------
	#Consider that:
	#1. there is a denser distribution of Experimental points 
	#2. In all cases (Except slow_1000C) exp_max>sim_max

	ind_upper_lim = h.index(Strain_sim, exp_max)[0] # Should equal 146
	#^Finds the simulated data point point that is closest to the experimental max strain.

	sizeOfResiduals = ind_upper_lim+1
	if (Strain_sim[ind_upper_lim]>exp_max):
		sizeOfResiduals -= 1
	#If the maximum Simulated strain data point after truncating is still larger than experimental max,
	#then I'll truncate the simulated stress a bit.


	#Set up zeros array for difference in stress and diff in strain:
	Stress_res = np.zeros(sizeOfResiduals)
	Strain_res = np.zeros(sizeOfResiduals)
	
	dy = np.zeros(sizeOfResiduals)

	#Fill the arrays with actual values of difference
	for n in range (sizeOfResiduals):
		ind_exp2 = h.index(Strain_exp , Strain_sim[n])[:2]
		ind_exp5 = h.index(Strain_exp , Strain_sim[n])
		#Find the indices of the experimental points nearest to the nth simulated point.
		
		avgExpStress = sum( Stress_exp[[ind_exp2]] )/2
		#^Average of the nearest two experimental data points' Stress.
		#This is a quite nested function so take a little time to appreciate it :)

		Stress_res[n] = Stress_sim[n] - avgExpStress
		Strain_res[n] = Strain_sim[n]
		
		dy[n] = np.std( Stress_exp[[ind_exp5]] )
		#Computes the nearest five experimental points' standard deviation.
		#Again, is a nested expression.
		ChiSqPerDoF = sum( (Stress_res/dy)**2 )/len(Stress_res)
		

	if __name__=="__main__":
		plt.title(r'$\chi^2$' +"=" +str(ChiSqPerDoF))	
		plotExp(Strain_exp, Stress_exp, fileName[0])
		plotSim(Strain_sim, Stress_sim, fileName[1])
		plotRes(Strain_res, Stress_res, dy)
		plotXYLegend()
		plt.suptitle(str(Temp)+ r'$^\degree$'+ "C")
		plt.show()
	return ChiSqPerDoF

	
def plotExp(Strain_exp, Stress_exp, inFile):
	t = str(inFile).split("/")[-1]
	plt.plot(Strain_exp, Stress_exp, label = t, marker= '.')	
	return
	
def plotSim(Strain_sim, Stress_sim, inFile):
	t = str(inFile).replace("t   ",'T=')\
		.replace("lj   ",'\n'+r'$\lambda_j$=')\
		.replace("gen   ",'\n'+r'$\rho_{gen}$=')\
		.replace("ann   ",'\n'+r'$\rho_{ann}$=')
	t = "(Simulated)"+t.split("/")[-1]
	plt.plot(Strain_sim, Stress_sim, label = t, marker= '.')
	return
	
def plotRes(Strain_res, Stress_res, dy):
	plt.errorbar(Strain_res, Stress_res, yerr=dy, label = "residual", marker = ',')
	#This ChiSqPerDoF value assumes dsigma = 1, which is not true.
	#Much more time is required for finding the ChiSqPerDoF value,
	#Which requires the use of s.d. of the 5 most nearby experimental values.
	return
	

def plotXYLegend():
	plt.legend(loc='right')
	plt.xlabel(r'$\varepsilon$')
	plt.ylabel(r'$\sigma$')
	return

	
if __name__ == "__main__":
	Temp = int(input("Temperature?"))
	speed = str(input("speed?"))
	y_n = input("Are you in a folder where everything is parallelized?(y/n)")
	#if y_n=="y": folder = "calibration_fixed/varying"+str(Temp)+"C_"+speed+"/"
	if y_n=="y": folder = "calibration_fixed/Varying"+str(Temp)+"C/"
	if y_n=="n": folder = "calibration_fixed/VaryingTwoVariables/"
	Residual(Temp, speed, folder)
