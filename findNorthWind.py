#Elias Stengel-Eskin
import os
import re
PD1 = True
a=4
b=5
if PD1:
	a = 3
	b = 4

def getSPS(lines):
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
				c = trim(lArr[b].strip())	
				#check if it's a vowel				
				regex = re.compile("[aeiouyEIOUY29@6]:?")
				m = re.match(regex, c)
				if m is not None:
					count +=1				
			line = lines[i]
	lArr = re.split("\\s", line)
	finalDur = int(lArr[a-o1])+int(lArr[a-o2])		
	finalDurSec = finalDur/SAM		
	SPS = count/finalDurSec
	return SPS


def wordTrim(word):
	word = word.replace("\"o", "ö")
	return word

def getSAM(lines):
	SAM = ""
	for i in range(len(lines)):
		if "SAM" in lines[i]:
			line = lines[i].split(" ")
			SAM = line[1]
	return int(SAM)
def trim(string):
	first = string.split("-") #deal with case where #U-U: etc, just get first
	string = first[0]
	string = re.sub("[^A-Za-z269@:~]", "", string) #remove any non-word characters
	return string


def getNW(path, NW):
	with open(path) as f1:
				lines = f1.readlines()
				i = 0
				

				for line in lines:
					i+=1
					if "Nordwind" in line:
						NW = True
						break
				if NW: #if north wind story
					#find line with "endlich"
					SAM = getSAM(lines)
					SPS = getSPS(lines)
					speakerInfo = []
					for i in range(len(lines)):
						if "REP" in lines[i]:
							speakerInfo.append(lines[i].split(" ")[1])
						if "SPN" in lines[i]:
							speakerInfo.append(lines[i].split(" ")[1])
						if "MAU" in lines[i]:
							if str(re.split("\\s", lines[i])[a])== str(70):
								line=re.split("\\s" ,lines[i])
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
					
								
								startTime2=nMARR[1]
								duration2 = nMARR[2] 
								
								firstStart = (int(startTime1)/int(SAM))
								secondStart = (int(startTime2)/int(SAM))
								firstEnd = (int(startTime1)+int(duration))/(int(SAM))
								secondEnd = (int(startTime2)+int(duration2))/(int(SAM))

								word = "gab"
								return("%s \t %f \t %f \t %s \t %f \t %f \t %s \t %f \t %s \t %s \t %s \t %s"%(character, firstStart, firstEnd, secondChar, secondStart, secondEnd, word, SPS, filename, speakerInfo[1].strip(), speakerInfo[0].strip().replace("ue", "ü"), "Second"))
end = "PD2"
if PD1:
	end = "PD1"								

regex = re.compile("[a-zA-Z0-9]+\.par,2")
NW = False
with open("/Users/elias/Desktop/PartiturParsing/NorthWind%s.txt"%(end), "w") as f2:
	for directory in os.walk("/Users/elias/Desktop/PartiturParsing/"+end, topdown=True):
			for filename in directory[2]:
				m = re.match(regex,filename)
				if m is not None:
					aaa = (getNW(directory[0]+"/" +filename , NW))
					if aaa is not None:
						f2.write(aaa + "\n")
