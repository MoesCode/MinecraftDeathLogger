#coding: utf-8
#Python 2.7

import re
import string
import time
import thread
import sys
import os

#--------------------------------Settings------------------------------------

logLocation = 'log.txt'		#where to find the server logs
langLocation = 'lang.txt'	#where to find the language file of MC
checkInterval = 3			#after how many seconds should be checked again

#----------------------------------Init--------------------------------------

allDeathMessages = []	#list for all possible death reasons
shouldRun = True	#to make process() terminatable
lastStop = 0	#saves where the file stopped reading to avoid unnecessary processing

#-------------------------------Useraction------------------------------------

'''the function actionOnDeath gets called, when a player dies. You can add whatever action you want to it, e.g. tweet the death'''



def actionOnDeath(deathMessage):
	print '[DEATH]', cleanName(deathMessage.group())	#prints the message
			



#-----------------------------Functions---------------------------------------

def runThroughFile():	#conveniently dont get old deaths on restart
	global lastStop		#reference global var lastStop
	f = open(logLocation)	#open the log
	f.seek(-1, os.SEEK_END)	#jump to the end of the file
	lastStop = f.tell()	#save where exactly that is
	f.close()	#close the file

def getDeathMessages():
	f = open(langLocation)	#language file
	for line in f:			#for every line in file
		if string.find(line,'death.') == 0:	#if line begins with 'death.'
			deathMessage = string.split(line,'=')	#separate the string
			deathMessage = deathMessage[1]	#get the useful part, not the part before the '='
			allDeathMessages.append(deathMessage)	#add it to the deaths for reference
	f.close()

def cleanDeathsMessages():		#strip vars out of strings
	global allDeathMessages	#reference global list allDeathMessages
	hlist = []			#placeholder list
	replaceVarWithRegEx = 	{					#replace vars with regex or null :P
								'%1$s':'([\w§]+)',	#1 is always the victim	#special case for § (coloured names)
								'%2$s':'(\w+)',	#2 is the killer
								'%3$s':'(\w+)',	#3 is the weapon
								'\n':'',		#newline gets removed...
							}	
	for message in allDeathMessages:		#in every message
		for replace in replaceVarWithRegEx.keys():	#for every unwanted string
			withThis = replaceVarWithRegEx[replace]	#get the counterpart
			message = string.replace(message,replace,withThis)	#replace it with specified replacement
		hlist.append(message)	#then add it to the list
	del hlist[30]	#removes duplicate entry (caused by same death message for slain by mob and slain by player)
	allDeathMessages = hlist	#replace the global list with the cleaned list

def cleanName(name):
	return re.sub('§.','', name)	#replaces all unwanted stuff with nothing
	
def scanForDeath(message):
	global lastStop
	for reason in allDeathMessages:	#for every reason
		match = re.search(reason, message)	#look for a match (a death message)
		if match != None:	#if there is one
			return match
	return None

def getNewDeaths():
	global lastStop	#reference global variable for cursor position
	newDeaths = []	#prepare list for all new deaths
	f = open(logLocation)	#open log file
	f.seek(lastStop)	#place cursor at last known position in log
	for line in f.readlines():	#for every new line (since last check)
		death = scanForDeath(line)	#check if the line contains a deathmsg
		if death != None:	#if yes
			newDeaths.append(death)	#add the message to the list
	lastStop = f.tell()	#mark this part as read
	f.close()
	for d in newDeaths:	#for every new death
		actionOnDeath(d)	#calls everything in the function
		

def process():
	global checkInterval
	while shouldRun:
		getNewDeaths()	#get any new death
		time.sleep(checkInterval)	#then sleep a while
	
def startProcess():
	t = thread.start_new_thread(process,())	#starts a new thread
	
def stopProcess():
	shouldRun = False	#cheap-ass termination

#--------------------------------Main---------------------------------------

if __name__ == '__main__':	#if the program has been started as standalone
	os.system('cls' if os.name=='nt' else 'clear')	#clear the terminal/logs
	print 'DeathTweeter has been started!'
	#runThroughFile()	#place cursor at end of log
	getDeathMessages()	#get all possible deathmessages
	cleanDeathsMessages()	#prepare them with RegEx'n shit
	startProcess()	#start the death checker
	while shouldRun:	#repeat during runtime
		s = raw_input('Write \'stop\' to end the program.\n')		#get input
		if s == 'stop':	#if input was 'stop'
			shouldRun = False	#stop the loops
			print 'Goodbye!'	#you dont need an explanation for this, do you?
			sys.exit()	#finally quite the program
		else:	#if input was not stop
			print 'Unknown command', s	#tell the user that it was wrong
