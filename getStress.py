#replaces ae, oe, ue with umlauts
def replaceUmlaut(string): 
	string = string.replace("ae", "ä")
	if "euer" not in string:
		string = string.replace("ue", "ü")
	string = string.replace("oe", "ö")
	return string
#replace ss with ß
def replaceSharp(string):
	oldString = string
	string = string.replace("ss", "ß")
	if oldString is string:
		return ""
	return string

def getStress(path):
	with open(path , "r") as f1:
		lines = f1.readlines()
	with open("stressOutput.txt" , "w") as f2:
		f2.write("orthography \t pattern \t index \t syllable number\n")
		for line in lines:
			split = line.split("\\")
			stressed = split[4] #this is the part w ' and -
			ortho = replaceUmlaut(split[1])
			Sortho = replaceSharp(ortho)
			syls = stressed.split("-") #split into syllables
			numString = ""
			numSyls = len(syls)
			index= 0
			for i in range(len(syls)):
				if "'" in syls[i]:
					numString = numString + "1"
					index = i+1
				else:
					numString = numString + "0"
			f2.write(ortho + "\t" + numString + "\t" + str(index) + "\t" + str(numSyls) + "\n")
			if Sortho is not "":
				f2.write(Sortho + "\t" + numString + "\t" + str(index) + "\t" + str(numSyls) + "\n")
			
getStress("/Users/elias/Desktop/gpw.cd")