import re
import sys
import os

def wordTrim(word):
	word = word.replace("\"o", "ö")
	return word

def trim(string):
	first = string.split("-") #deal with case where #U-U: etc, just get first
	string = first[0]
	string = re.sub("[^A-Za-z269@:~]", "", string) #remove any non-word characters
	return string


def parseFile(path):
	fileArr = path.split("/")
	fileName = fileArr[len(fileArr)-1]
	with open(path, "r") as f1:
		lines = f1.readlines()
	with open("/Users/elias/Desktop/CelexParsing/wordTypeOutput.txt", "r") as f2:
		#get all the function/closed words/categories
		excludeLines = f2.readlines()
	i = 0
	isStop = False
	word = ""
	SAM = ""
	for l in lines: #only go past 1 undesireable word

		if "ORT" in l and i<2:
			i=i+1 #counter keeps track of how many times you've gone through
			word = l.split("\t")[2].strip() #get orthographic word
			found = False
			for line in excludeLines:
				if word.strip() == line.strip(): #if it's one of the lines you don't want
					found = True #look at the next word
					break
			if found:
				
				continue
			#now word is not undesirable, check if it starts w stop
			if word[0] in {"p","t","k","b","d","g"}:
				
				isStop = True
				break
			else:
				
				isStop = False
				break
	#now do the hard work
	if isStop:
		#lets get the LBO
		start = 0
		end = 0
		for i in range(len(lines)):
			if "SAM" in lines[i]:
				line = lines[i].split(" ")
				SAM = line[1]
				#gets correct SAM
			if "LBO" in lines[i] and word in lines[i]: # you found the right line
				line = lines[i].split(" ")
			
				numbers = line[1]
				start = numbers.split(",,")[0]
				end = numbers.split(",,")[1]

				
			if "PHO" in lines[i] and str(start) in lines[i]: #now look for the PHO of the first word
				
				line = lines[i].split("\t")
				if line[2] == "0":
					continue
				 #successfully gets the right PHO line
				character = line[4].strip()
				character = trim(character)
			
				#get start and end sample times
				startTime1=line[1]
				duration = line[2] 
				#TODO: get the next vowel, start time, end time, etc
				nextPHO = lines[i+1]
				
				nPARR = nextPHO.split("\t")
				
				secondChar = trim(nPARR[4].strip())
				
				
				regex = re.compile("[aeiouyEIOUY29@6]:?")
				m = re.match(regex, secondChar)
				if m is not None:
					#continue on, get times
					startTime2=nPARR[1]
					duration2 = nPARR[2] 
				else:
					#you're done, forget it
					break
				
				firstStart = (int(startTime1)/int(SAM))
				secondStart = (int(startTime2)/int(SAM))
				firstEnd = (int(startTime1)+int(duration))/(int(SAM))
				secondEnd = (int(startTime2)+int(duration2))/(int(SAM))

				word = wordTrim(word)
				return "%s \t %f \t %f \t %s \t %f \t %f \t %s \t %s"%(character, firstStart, firstEnd, secondChar, secondStart, secondEnd, word, fileName)

#parseFile("/Users/elias/Desktop/PD2/awe/awed5050.par,2")

regex = re.compile("[a-zA-Z0-9]+\.par,2")
with open("/Users/elias/Desktop/partiturOutput.txt" , "w") as f3:
	#all the files in the directory
	for directory in os.walk("/Users/elias/Desktop/PD2", topdown=True):
		for filename in directory[2]:
			#make sure it ends in .par,2
			m = re.match(regex,filename)
			if m is not None:
				#run the parseFile method
				toWrite = parseFile(directory[0]+"/" +filename)
				if toWrite is not None:
					#write to file
					f3.write(toWrite + "\n")

