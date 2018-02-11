#!C:\Users\Ocean\AppData\Local\Programs\Python\Python36-32\python.exe
import glob
import os
import subprocess as sp
import time
import header as h

def justReadTheInput(Temp):
	f = open("./calibration_fixed/INPUT.txt" , 'r')
	Lines = f.readlines()
	for line in Lines:
		if line=='\n': del line
	T_off = findT_off(Temp, 'slow')[0]
	return (Lines[T_off],Lines[T_off+1],Lines[T_off+2])

def findT_off(T, speed):
	T_off = 1 #for error checking purpose
	if(T ==1000): 
		T_off= 0
		p_T = 8.1E-8
		orderToEndAt = 1
		if(speed=="fast"):orderToEndAt = 6
	if(T ==900): 
		T_off = 3
		p_T = 6.0E-8
		orderToEndAt = 2
		if(speed=="fast"):orderToEndAt = 7
	if(T ==800): T_off = 6; p_T = 5.5E-8; orderToEndAt = 3
	if(T ==700): T_off = 9; p_T = 5.0E-8; orderToEndAt = 4
	if(T ==600): T_off = 12;p_T = 4.5E-8; orderToEndAt = 5
	#Error checking: since T must be one of the above values,
	#(cause I'm pedantic)
	if(T_off ==1): #If T_off remained unchanged after these lines of code, raise error.
		raise ValueError #And say fuck you to the user!
	return (T_off, orderToEndAt)
	
	
def rewriteInput_TwoVar(gen, ann):
	#Store the whole INPUT.txt file in memory
	f = open("./calibration_fixed/INPUT.txt" , 'r+')
	Lines = f.readlines() 
	for line in Lines:
		if line=='\n': del line
		#clear the empty lines
		
	#changed the three variables,
	Lines[1] = str(gen)+'\n'
	Lines[4] = str(gen)+'\n'
	Lines[7] = str(gen)+'\n'
	Lines[10]= str(gen)+'\n'
	Lines[13]= str(gen)+'\n'
	Lines[2] = str(ann)+'\n'
	Lines[5] = str(ann)+'\n'
	Lines[8] = str(ann)+'\n'
	Lines[11]= str(ann)+'\n'
	Lines[14]= str(ann)+'\n'
	
	#and then delete the file.
	f.seek(0)
	f.truncate()

	#re-write file with changed variables
	wholeFile = ''
	for line in Lines:
		if line!='\n': wholeFile += line
	f.write(wholeFile)
	f.close()

def rewriteInput_lj(Temp, speed, lj):
	Temp = int(Temp)
	speed = str(speed)
	lj = float(lj)
	
	(T_off, orderToEndAt) = findT_off(Temp, speed)
	
	#Store the whole INPUT.txt file in memory
	f = open("./calibration_fixed/INPUT.txt" , 'r+')
	Lines = f.readlines() 
	for line in Lines:
		if line=='\n': del line
		#clear the empty lines

	Lines[T_off] = str(lj)+'\n'
	
	#and then delete the file.
	f.seek(0)
	f.truncate()

	#re-write file with changed variables
	wholeFile = ''
	for line in Lines:
		if line!='\n': wholeFile += line
	f.write(wholeFile)
	f.close()
	return orderToEndAt
	
def RemoveElastic_Rewrite(originalPath, textFileName, folder):
	while(sum(1 for line in open(originalPath))<147):time.sleep(0.5)
	#Very important: wait until file is fully written before extracting data!
	
	f = open(originalPath, 'r')
	Lines = f.readlines()
	f.close()
	
	os.remove(originalPath)
	os.chdir(folder)
	
	print(os.getcwd())
	
	#o.write("data that has removed elastic part")
	
	o = open(textFileName, 'w')
	Stress = []
	Strain = []
	for line in Lines:
		Strain.append(float(line.split()[0]))
		Stress.append(float(line.split()[1]))
	E = (Stress[1]-Stress[0])/(Strain[1]-Strain[0])
	for n in range (len(Lines)-1):
		N = n+1 #shift everything one line up
		newStrain=Strain[N]-Strain[1]
		#newStrain=Strain[N]-Stress[N]/E)
		o.write(str(newStrain))
		#print(str(Strain[N]-Stress[N]/E))
		o.write("\t")
		o.write(str(Stress[N]))
		o.write("\n")
	print("Done writing the new stress to file, closing it now...")
	o.close()
	os.chdir("..")
	return
	
def runExecutable(folder, orderToEndAt):
	os.chdir("./calibration_fixed/")
	q = sp.Popen(["./sxmodel.exe"])
	#Call the executable

	#loop once for each of the following temperature:
	Temperatures = [1000, 900, 800, 700, 600, 1000, 900]
	del Temperatures[orderToEndAt:]
	speed = ["slow",]*5+["fast",]*2

	#make a folder
	if not os.path.exists(folder):
		os.makedirs(folder)
		print("Making folder", folder)

	
	for order in range (len(Temperatures)):
		Temp = Temperatures[order]
		print("TemperatureTEMPERATURE==========================================================================================",Temp)
		#Check every 0.2 second that this file haven't came into existance yet.
		expectantFilePath= r'./'
		while (h.getFilePath(Temp, expectantFilePath )==[]): time.sleep(0.2)
		print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAND we are done waiting!")
		Path_orig = str(h.getFilePath(Temp, expectantFilePath )[0])
		textFileName = "Sim"+str(Temp)+"C_"+speed[order]+".txt"
		time.sleep(1.5) #1.5s is just enough time for sxmodel.exe to print; but not enough for a new job to start.
		RemoveElastic_Rewrite(Path_orig, textFileName, folder)

	q.kill()
	os.chdir("..")	
	return

if __name__ == '__main__':
	folder = str(input("Folder name?"))
	runExecutable(folder)
