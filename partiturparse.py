#Elias Stengel-Eskin
import re
import sys
import os
PD1 = False

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
	p = 0
	isStop = False
	word = ""
	index = 0
	SAM = ""
	LBOindex = 0
	wordindex = 0
	for l in lines: #only go past 1 undesireable word
		wordindex = p
		if "ORT" in l and i<2:
			i=i+1 #counter keeps track of how many times you've gone through
			word = l.split("\t")[2].strip() #get orthographic word
			index = int(l.split("\t")[1])

			found = False
			for line in excludeLines:
				
				if word.strip() == line.strip(): #if it's one of the lines you don't want
					found = True #look at the next word
					break
			if found:
				
				p+=1	
				continue
			#now word is not undesirable, check if it starts w stop
			if word[0] in {"p","t","k","b","d","g"}:	
				isStop = True

				break
			else:	
				isStop = False
				break
		p+=1 
	 #wordindex is line number of the word
	#now do the hard work
	if isStop:
		
		#lets get the LBO
		start = 0
		end = 0
		a = 4
		b = 5
		if PD1:
			a = 3
			b = 4
		for i in range(len(lines)):
			if "SAM" in lines[i]:
				line = lines[i].split(" ")
				SAM = line[1]
								#gets correct SAM
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
				firstStart = (int(startTime1)/int(SAM))
				secondStart = (int(startTime2)/int(SAM))
				firstEnd = (int(startTime1)+int(duration))/(int(SAM))
				secondEnd = (int(startTime2)+int(duration2))/(int(SAM))

				word = wordTrim(word)
				return "%s \t %f \t %f \t %s \t %f \t %f \t %s \t %s"%(character, firstStart, firstEnd, secondChar, secondStart, secondEnd, word, fileName)
#print(parseFile("/Users/elias/Desktop/PD2/dlm/dlma5340.par,2"))

regex = re.compile("[a-zA-Z0-9]+\.par,2")
end = "PD2"
if PD1:
	end = "PD1"
with open("/Users/elias/Desktop/partiturOutput%s.txt"%(end) , "w") as f3:
	#all the files in the directory
	
	for directory in os.walk("/Users/elias/Desktop/"+end, topdown=True):
		for filename in directory[2]:
			#make sure it ends in .par,2
			m = re.match(regex,filename)
			if m is not None:
				#run the parseFile method

				toWrite = parseFile(directory[0]+"/" +filename)
				if toWrite is not None:
					#write to file
					f3.write(toWrite + "\n")

