#Elias Stengel-Eskin
import re
import sys
import os
PD1 = True

SAM = 16000

def getSpeakerInfo(speaker):
	sex = "M"
	age = "young"
	PD2name = "" 
	end = "PD2"
	if PD1:
		end = "PD1"
	with open("/Users/elias/Desktop/PartiturParsing/%s_sprk.txt"%end) as s:
		speakers = s.readlines()
	for line in speakers:
		lArr = re.split("\\s", line)
		if speaker.upper() == lArr[1]:
			#it's the right speaker
			if lArr[3] == "W":
				sex = "F"
			if lArr[4] == "A":
				age = "old"
		try:
			PD2name = lArr[5]
		except:
			PD2name = "N/A"
		if PD2name == "":
			PD2name = "N/A"
	return (speaker, sex, age, PD2name)

def wordTrim(word):
	word = word.replace("\"o", "ö")
	return word

def trim(string):
	first = string.split("-") #deal with case where #U-U: etc, just get first
	string = first[0]
	string = re.sub("[^A-Za-z269@:~]", "", string) #remove any non-word characters
	return string
#gets the sampling rate
def getSAM(lines):
	
	SAM = ""
	for i in range(len(lines)):
		if "SAM" in lines[i]:
			line = lines[i].split(" ")
			SAM = line[1]
	return int(SAM)

def getSylNum(lines, index):
	regex = re.compile("[aeiouyEIOUY29@6]:?")
	count=0
	a=4
	b=5
	if PD1:
		a = 3
		b = 4
	for line in lines:
		lArr = re.split("\\s", line)
		if "MAU" in line and str(lArr[a]) == str(index) :
			m = re.match(regex, lArr[b])
			if m is not None:
				count+=1
	return count
def getLastPhoneme(lines):
	a=4
	b=5
	if PD1:
		a = 3
		b = 4
	last = ""
	for line in lines:
		lArr= re.split("\\s" , line)
		if "MAU" in line and str(lArr[a]) == str(0):
			last = lArr[b]
	return last
#gets the syllables per second
def getSPS(lines):
	maxIndex = 0
	SAM = getSAM(lines)
	line = ""
	count = 0
	a=4
	b=5
	o1 = 3
	o2 = 2
	if PD1:
			a = 3
			b = 4
			o1 = 2
			o2 = 1
	#get syllables/second
	for i in range(len(lines)):		
		if "MAU" in lines[i]:  
			lArr = re.split("\\s", lines[i])
			if "MAU" not in lines[i-1] and str(lArr[a]) == str(-1):				
				#this is the first -1, ignore it
				continue
			try:
				if "MAU" not in lines[i+1] and str(lArr[a]) == str(-1):					
					#this is a last -1, ignore it
					continue
			except:
				if "MAU" in lines[i] and str(lArr[a]) ==str(-1):					
					continue
			else:
				if int(lArr[a]) > int(maxIndex):
					maxIndex = int(lArr[a])
				c = trim(lArr[b].strip())	
				#check if it's a vowel				
				regex = re.compile("[aeiouyEIOUY29@6]:?")
				m = re.match(regex, c)
				if m is not None:
					count +=1				
			line = lines[i]
	lArr = re.split("\\s", line)
	finalDur = int(lArr[a-o1])+int(lArr[a-o2])	
	finalDurSec = 1
	if SAM == 0:
		SAM = 16000	
	finalDurSec = finalDur/SAM
		
	SPS = count/finalDurSec

	return (SPS, count, maxIndex)


def getStress(lines, index):
	for line in lines:
		lArr = re.split("\\s", line)
		if "KAN" in line and str(lArr[1]) == str(index):
			wordArr = lArr[2].split('\'')
			
			regex = re.compile(".*[aeiouyEIOUY29@6]:?.*")
			m = re.match(regex, wordArr[0])
			if m is None:
				return True
			else:
				return False			
	return False

def getWordTimes(lines, index):
	SAM = getSAM(lines)
	if SAM == 0:
		SAM = 16000	
	startSec = 1000
	endSec = 0
	a=4
	b=5
	o1 = 3
	o2 = 2
	if PD1:
		a = 3
		b = 4
		o1 = 2
		o2 = 1

	for i in range(len(lines)):		
		if "MAU" in lines[i]:  
			lArr = re.split("\\s", lines[i])
			if str(lArr[a]) == str(index):
				
				if (int(lArr[1])/SAM)<startSec:
					#print(lArr[1] + " is start ")
					startSec = int(lArr[1])/SAM
				if (int(lArr[a-o1])+int(lArr[a-o2]))/SAM>endSec:
					#print( "%d+%d is end "%(int(lArr[a-o1]),int(lArr[a-o2])))
					endSec = (int(lArr[a-o1])+int(lArr[a-o2]))/SAM
				
	return (startSec, endSec)

def getInfo(lines, didSkip, index, word, speakerInfo, fileName, preceding):
	lastPhon = ""
	precType = "Content"
	if didSkip:
		precType = "Function"
	if index !=0:	
		lastPhon = getLastPhoneme(lines)

	wordTup = getWordTimes(lines, index)
	wordStart = wordTup[0]
	wordEnd = wordTup[1]
	#lets get the LBO
	start = 0
	end = 0
	a = 4
	b = 5
	
	if PD1:
		a = 3
		b = 4

	SPSTup = getSPS(lines)
	SPS = SPSTup[0]
	
	numWords = SPSTup[2]

	SAM = getSAM(lines)
	if SAM == 0:
		SAM = 16000	
	#gets correct SAM
	for i in range(len(lines)):
		#look for the MAU of the first or second word
		if "MAU" in lines[i] and str(re.split("\\s", lines[i])[a]) == str(index):		

			line = re.split("\\s", lines[i])
			#catch weird stuff 
			if line[2] == "0":
				continue
			if line[1] == "0":
				continue
			character = "z"
			
			character = line[b].strip()
			
			character = trim(character)			
			#get start and end sample times
			startTime1=line[1]
			duration = line[2] 
			#TODO: get the next vowel, start time, end time, etc
			nextMAU = lines[i+1]				
			nMARR = re.split("\\s", nextMAU)	
				
			secondChar = trim(nMARR[b].strip())	
				
			regex = re.compile("[aeiouyEIOUY29@6]:?")
			m = re.match(regex, secondChar)
			if m is not None:
				#continue on, get times
				startTime2=nMARR[1]
				duration2 = nMARR[2] 
			else:
				#you're done, forget it
				break
			firstStart = 0
			secondStart = 0
			firstEnd = 0
			secondEnd=0
			
			firstStart = (int(startTime1)/int(SAM))
			secondStart = (int(startTime2)/int(SAM))
			firstEnd = (int(startTime1)+int(duration))/(int(SAM))
			secondEnd = (int(startTime2)+int(duration2))/(int(SAM))
			
			word = wordTrim(word)
			skip = "Initial"
			if didSkip:
				skip = "Second"
			if index != 0:
				skip = "Second"

			speakerTup = getSpeakerInfo(speakerInfo[1].strip())
			sex = speakerTup[1]
			age = speakerTup[2]
			PD2name = speakerTup[3]
			sylCount = getSylNum(lines, index)

			return "%s,%f,%f,%s,%f,%f,%s,%f,%f,%d,%f,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"%(character, firstStart, firstEnd, secondChar, secondStart, secondEnd, word, wordStart, wordEnd, sylCount, SPS, numWords+1, fileName, speakerInfo[1].strip(), speakerInfo[0].strip().replace("ue", "ü"), skip, precType, preceding, lastPhon,sex,age,PD2name)
		

def parseFile(path):
	fileArr = path.split("/")
	fileName = fileArr[len(fileArr)-1]
	fileName = fileName[:len(fileName)-6] #get rid of the .par,2
	with open(path, "r") as f1:
		lines = f1.readlines()
	with open("/Users/elias/Desktop/CelexParsing/wordTypeOutput.txt", "r") as f2:
		#get all the function/closed words/categories
		excludeLines = f2.readlines()
	speakerInfo = []

	preceding = ""
	
	i = 0
	p = 0
	isStopFirst = False
	isStopSecond = False
	isContentFirst = True
	isContentSecond = True
	word = ""
	index = 0
	index2 = 0
	didSkip = False
	LBOindex = 0
	wordindex = 0

	
	for j in range(len(lines)): #only go past 1 undesireable word
		l = lines[j]
		if "REP" in l:
			speakerInfo.append(l.split(" ")[1])
		if "SPN" in l:
			speakerInfo.append(l.split(" ")[1])
		if "ORT" in l:
			word = l.split("\t")[2].strip() #get orthographic word
			index = int(l.split("\t")[1])
			word2 = ""
			try:
				word2 = lines[j+1].split("\t")[2].strip()
				index2 = int(lines[j+1].split("\t")[1].strip())
			except:
				print("only 1 word in file " + path)
			

			found = False

			for line in excludeLines:
				
				if word.strip() == line.strip(): #if it's one of the lines you don't want
					preceding = word.strip()
					found = True #look at the next word
					break
			
			for line in excludeLines:
				if word2.strip() == line.strip():
					isContentSecond = False
					break

			if found:
				didSkip = True
				isContentFirst = False
				p+=1	
			break
				
			#now word is not undesirable, check if it starts w stop
	stopRegex = re.compile("[pP]|[bB]|[gG]|[kK]|[tT]|[dD]") #changed to regex to include capital letters

	m = re.match(stopRegex, word[0])
	if m is not None:	

		isStopFirst = True
				
	else:	
		isStopFirst = False
				
	m2 = re.match(stopRegex, word2[0])
	if m2 is not None:
	
		isStopSecond = True
		
	else:
		isStopSecond = False	
	 #wordindex is line number of the word
	
	firstLine = None
	secondLine = None
	#now do the hard work
	if isStopFirst and getStress(lines,index) and isContentFirst:
		firstLine = getInfo(lines, didSkip, index, word, speakerInfo, fileName, preceding)
		#print(firstLine)
		
	if isStopSecond and getStress(lines, index2) and isContentSecond and index2 !=0:
		preceding = word
		secondLine = getInfo(lines, didSkip, index2, word2, speakerInfo, fileName, preceding)
		
	#print(firstLine)
	#print(secondLine)
	return(firstLine, secondLine)
			
#print(parseFile("/Users/elias/Desktop/PartiturParsing/PD1/ANFN/anfn2150.par,2"))


regex = re.compile("[a-zA-Z0-9]+\.par,2")
end = "PD2"
if PD1:
	end = "PD1"
with open("/Users/elias/Desktop/partiturOutput%s.txt"%(end) , "w") as f3:
	#all the files in the directory
	
	for directory in os.walk("/Users/elias/Desktop/PartiturParsing/"+end, topdown=True):
		for filename in directory[2]:
			#make sure it ends in .par,2
			m = re.match(regex,filename)
			if m is not None:
				#run the parseFile method

				toWrite = parseFile(directory[0]+"/" +filename)
				if toWrite[0] is not None:
					#write to file
					f3.write(toWrite[0] + "\n")
				if toWrite[1] is not None:

					f3.write(toWrite[1] + "\n")
					

