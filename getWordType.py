import re
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


def getWordType(path):
	with open(path, "r") as f1:
		lines = f1.readlines()
	with open("/Users/Elias/Desktop/output2.txt" , "w") as f2:
		for line in lines:
			split = line.split("\\")
			
			if split[3] in {"3", "5", "6", "8"}:
				split[1] = replaceUmlaut(split[1])
				sharp = replaceSharp(split[1])
				f2.write(split[1] + "\n")
				if sharp is not "":
					f2.write(sharp + "\n")
getWordType("/Users/Elias/Desktop/gsl.cd")


