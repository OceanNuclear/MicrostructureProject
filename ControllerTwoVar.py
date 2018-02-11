#!C:\Users\Ocean\AppData\Local\Programs\Python\Python36-32\python.exe
import os
import Fitter as Fi
import numpy as np
import subprocess as sp
from scipy.optimize import curve_fit
import Supervisor as Su


#Making a counter
Ith = 0
def incr(): #For counting purpose
	global Ith
	Ith = Ith + 1
	print("iterating",Ith, "time...")
	return
	

#--------------------make up file name, and open it------------------------
#Make up the folder path name to the Simulated data


#Optional: Run the executable once to ensure the Reference data is reasonable (though it won't be actually read)
#Su.runExecutable("Reference1")


'''
Here I'm forcing curve_fit function to "move" the input values given to the residuals-printing function Fi.Residual() (which the Fi.Residual() reads from file anyways) to match a bunch of y = 0; so by "moving" the input values, I mean to write them down to file, and then run the .exe that turns these input values into output curves; and wait until the .exe has finished running.

Not the smartest move, I know, but this is the best hack that i came up with while working just an executable and no original function.
'''




#orderToEndAt = Su.rewriteInput_lj()
y_target = [0,]*6
	
def FuncFitting_alignTwoVar(x, gen, ann): #this function finds the optimal value of gen and ann to minimize the residuals
	#For the user's inspection:
	print("Guessing gen=", gen)
	print("Guessing ann=", ann)
	
	Su.rewriteInput_TwoVar(gen, ann)

	incr()#increase the counter, ready to start the .exe.
	
	#Wait for the executable to run,
	orderToEndAt = 7
	folderName = "VaryingTwoVariables/"
	
	Su.runExecutable(folderName, orderToEndAt)

	Chi = np.zeros(6)
	
	#calculate the residual of the file retrieved from the same folder
	Chi[0] = np.sqrt(Fi.Residual(1000, 'slow', str("./calibration_fixed/"+folderName)))
	Chi[1] = np.sqrt(Fi.Residual( 900, 'slow', str("./calibration_fixed/"+folderName)))
	Chi[2] = np.sqrt(Fi.Residual( 800, 'slow', str("./calibration_fixed/"+folderName)))
	Chi[3] = np.sqrt(Fi.Residual( 700, 'slow', str("./calibration_fixed/"+folderName)))
	Chi[4] = np.sqrt(Fi.Residual(1000, 'fast', str("./calibration_fixed/"+folderName)))
	Chi[5] = np.sqrt(Fi.Residual( 900, 'fast', str("./calibration_fixed/"+folderName)))
	return Chi
p_initialGuess= Su.justReadTheInput(1000)[1:]
boundary = ([1E-6, 1E-3], [1E-3, 1E-1])
popt, pcov = curve_fit( FuncFitting_alignTwoVar, 0, y_target, p0 = p_initialGuess, bounds = boundary)

#Unpacking variables.
(gen , ann ) = popt
(var_a,dummy), (dummy, var_b) = pcov
da, db = np.sqrt((var_a, var_b))
print("gen=",gen,"+\-",da)
print("ann=",ann,"+\-",db)
print("Number of iterations =" , Ith)
