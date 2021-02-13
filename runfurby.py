#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import subprocess
import os
from random import randint
from os import listdir
from os.path import isfile, join
from subprocess import call
import audioop
import pyaudio

myrmsavg = 0
myrmstotal = 0
mylevel = 700
SAMPLING_RATE = 22050
NUM_SAMPLES = 1024
os.system('clear')


##bored timer in seconds.. executes playrandom or sayrandom
## 999999 for none
boredtime = 120


### content folder #####
homefolder = "/home/pi/responsedata/"

#sayrandom content is collection of short text files in homefolder above.
#playrandom content is collection of short mp3 or wav files in homefolder above.

### uncomment only 1 to pick say or play ###
#myaction= "sayrandom"
myaction= "playrandom"


################ No config below here..just pain.. ################

os.system("flite -voice rms -t '..., ...'")                
os.system("flite -voice rms -t 'Setting sound levels'")              

#### turn on the microphone
subprocess.call("amixer set Capture Volume 70%  >> /dev/null", shell=True)

############### Set Ambient Levels #################
x=1
os.system('clear')
while (x <=10):
    time.sleep(.15)
    _stream = None
    myrms = 0
    pa = pyaudio.PyAudio()
    _stream = pa.open(format=pyaudio.paInt16, channels=2, rate=SAMPLING_RATE,input=True, frames_per_buffer=NUM_SAMPLES)
    data = _stream.read(NUM_SAMPLES)
    myrms = audioop.rms(data, 2)
    myrmstotal = myrmstotal + myrms
    pa.close(_stream)
    myrmsavg = int(myrmstotal / x)
    os.system('clear')
    print("Getting Ambient Sound Level")
    print("######################################################################")
    print("Abmient Sound Level Average : " + str(myrmsavg))
    print("Current RMS : " + str(myrms) + "  Running Total : " + str(myrmstotal))
    print("######################################################################")
    x=x+1

mytriggerlevel = int(myrmsavg * 1.5)
os.system('clear')
print("Ambient Sound Level Set")
print("######################################################################")
print("Abmient Sound Level Average : " + str(myrmsavg))
print("Setting Trigger Sound Level To : " + str(mytriggerlevel))
print("######################################################################")
time.sleep(3)
############### END Set Ambient Levels #################

os.system('clear')

################## Say Random Action Function ##############
def sayrandom():
	mynow = time.time()
	mythen = time.time()	

	# crazy pick a random file magic
	myfiles = listdir(homefolder)
	myfilecount = len(myfiles)
	randomizer=randint(0,myfilecount-1)
	randomfile = myfiles[randomizer]
	myresponse = homefolder + randomfile
	mytalk = ""
	with open(myresponse) as v:
		for line in v:
			line = line.replace("'","")
			mytalk = mytalk+ line

	#clear and print
	os.system('clear') 							
	print ("----------------------------------")
	print(mytalk)
	print ("----------------------------------")																					
	#turn off the mic while talking							
	subprocess.call("amixer set Capture Volume 0%  >> /dev/null", shell=True)

	#talk
	os.system("flite -voice rms -t '..., ...'")                
	os.system("flite -voice rms -t '"+mytalk+"'")                

	#wait a sec to prevent setting it off with the response
	time.sleep(1)

	#turn mic back on
	subprocess.call("amixer set Capture Volume 70%  >> /dev/null", shell=True)

	#clear vars for good measure
	mytalk = ""
	myresponse = ""
	return
##################END Say Random Action##############
				
##################Play Random Action##################
def playrandom():
	mynow = time.time()
	mythen = time.time()	

	os.system('clear') 							
	print ("----------------------------------")

	# crazy pick a random file magic
	myfiles = listdir(homefolder)
	myfilecount = len(myfiles)
	randomizer=randint(0,myfilecount-1)
	randomfile = myfiles[randomizer]
	myresponse = homefolder + randomfile

	## turn off the mic
	subprocess.call("amixer set Capture Volume 0%  >> /dev/null", shell=True)
	
	print ("----------Playing File------------")
	print (myresponse)
	print ("----------------------------------")
	
	##play the random file
	os.system("ffplay -nodisp -autoexit -loglevel quiet '"+myresponse+"' >>/dev/null")

	#wait a sec to prevent setting it off with the response
	time.sleep(1)

	## turn mic back on
	subprocess.call("amixer set Capture Volume 70%  >> /dev/null", shell=True)
	os.system('clear') 								
	return
##################END Play Random Action##################


### system ready notification ###
os.system("flite -voice rms -t '..., ...'")                
os.system("flite -voice rms -t 'System online, say something'")              

os.system('clear') 							
print ("----------------------------------")
print ("--------##Listening##-------------")
print ("----------------------------------")

#start up bored timer
mynow = time.time()
mythen = time.time()

######### System Loop - program start #########
while True:
	#give the pc a breather between loops
	time.sleep(.25)
	#checking if bored time has elapsed
	mynow = time.time()
	if(mynow > mythen+boredtime):
		mynow = time.time()
		mythen = time.time()	
		if (myaction == "playrandom"):
			playrandom()
		else:
			sayrandom()

	#set up audio insanity
	_stream = None
	myrms = 0
	pa = pyaudio.PyAudio()
	_stream = pa.open(format=pyaudio.paInt16, channels=2, rate=SAMPLING_RATE,input=True, frames_per_buffer=NUM_SAMPLES)
	data = _stream.read(NUM_SAMPLES)
	myrms = audioop.rms(data, 2)
	pa.close(_stream)
	#check if rms level is above the trigger
	if(myrms > mytriggerlevel):

		#heard something, start the furby motor - external script startfurby.py
		subprocess.call("sudo python3 /home/pi/startfurbymotor.py", shell=True)

		#do say or playrandom as selected in the options at top
		if(myaction =="playrandom"):      
			playrandom()
			#done playing stop furby motor - external script stopfurby.py
			subprocess.call("sudo python3 /home/pi/stopfurbymotor.py", shell=True)		
			os.system('clear') 							
			print ("----------------------------------")
			print ("--------##Listening##-------------")
			print ("----------------------------------")

		if(myaction =="sayrandom"):      
			sayrandom()
			#done playing stop furby motor - external script stopfurby.py
			subprocess.call("sudo python3 /home/pi/stopfurbymotor.py", shell=True)		
			os.system('clear') 							
			print ("----------------------------------")
			print ("--------##Listening##-------------")
			print ("----------------------------------")
			#time.sleep(.5)
	myrms = 0
	os.system('clear') 							
	print ("----------------------------------")
	print ("--------##Listening##-------------")
	print ("----------------------------------")		
			
#########END program loop return to while True: #########    
