# Task
Microstructure modelling project in Spring term 2018. This repository contains scripts and results of two tasks:

## Calibration
A windows executable was given, which takes in 3 parameters as input and creates a force-displacement curve as the output.
The objective is to find the set of parameters that gives a curve that fits most closely to the reference curve, and verify that it fits those 3 parameters used to generate this reference curve.

## curve fitting
10 experimental force-displacement curves were given (600 - 1000 degrees Celcius at 100 degrees step size, at either fast or slow strain rate, ); the set of 3 parameters that best fit each of those curve were needed.

# Method
A Python function does the following: write the input file for the executable, call the executable using os.system(), wait for the executable to finish running, read the resulting file, delete it, then compare the values read against the expected curve, and return the residuals.
The numpy optimizer uses this function as the objective function to be minimized.

Parallel processing was needed to speed up the program; but this was done by simply opening a new instance of the command line and calling the python script with a slightly different input.
