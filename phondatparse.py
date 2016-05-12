#Elias Stengel-Eskin
import re
import os
import sys
from collections import defaultdict
from textgrid import TextGrid, IntervalTier


PD1 = True
a = 3
b = 4		

class Seg(object):
	def __init__(self, start, end, segment, index):
		self.segment = segment
		self.start = start
		self.end = end
		self.index = index

def getSAM(lines):
	SAM = ""
	for i in range(len(lines)):
		if "SAM" in lines[i]:
			line = lines[i].split(" ")
			SAM = line[1]
	return int(SAM)

def getMAU(lines, SAM, filename):
	allMAU = []
	for line in lines:
		if "MAU" in line and "-1" not in line:
			l = re.split("\\s+", line)
			try:
				segStart = int(l[1])/SAM
				segEnd = round((int(l[1]) + int(l[2]))/SAM,2)
			
				segment = l[b]
				index = l[a]
				seg = Seg(segStart, segEnd, segment, index)
				allMAU.append(seg)
			except ZeroDivisionError:
				print("no SAM at%s"%filename)
				return None
	return allMAU

def getMaxTime(allMAU):
	maxtime = -1
	try:
		maxtime = float(allMAU[0].start) + float(allMAU[len(allMAU)-1].end)
	except IndexError:
		print("indexerror occured ")
	
	return maxtime

def getWords(lines, allMAU, filename):
	#word, start, end
	words = []
	word = ""
	start = 0
	end = 0
	i = 0
	for line in lines:
		if "ORT" in line:
			l = re.split("\\s+", line)
			word = l[2]
			index = l[1]
			#get first and last segment for start/end
			for i in range(len(allMAU)):
				if str(index) == str(allMAU[i].index):
					start = allMAU[i].start				
					break	
			while i < len(allMAU)-1:
				i+=1
				if str(index) != str(allMAU[i].index):
					i-=1
					break
			try:
				end = allMAU[i].end
			except IndexError:
				print("indexerror occured at %s %s %s"%(filename, word, index))
			tup = (start, end, word)
			words.append(tup)
	return words


#get the info we want from the Seg (no index)
def getSegInfo(Seg):
	toreturn = (Seg.start, Seg.end, Seg.segment)
	return toreturn

def parseFile(path, fn):
	filename= fn.split(".")[0] #just name of file
	with open(path, "r") as f1:
		lines = f1.readlines()
	SAM = getSAM(lines)
	allSegs = getMAU(lines, SAM, filename)
	if allSegs is None:
		return
	segs = []
	for seg in allSegs:
		
		#print("%f %f %s %s"%(seg.start, seg.end, seg.segment, seg.index))
		tup = getSegInfo(seg)
		segs.append(tup)
	words = getWords(lines, allSegs, filename)


	maxtime = getMaxTime(allSegs)
	if maxtime == -1:
		return
	tg = TextGrid(maxTime = maxtime)
	wordtier = IntervalTier(name = 'words', maxTime = maxtime)
	phonetier = IntervalTier(name = 'phones', maxTime = maxtime)
	for interval in words:
		wordtier.add(*interval)
	for interval in segs:
		phonetier.add(*interval)
	tg.append(wordtier)
	tg.append(phonetier)
	outpath = "/Users/elias/Desktop/TextGrids/%s.TextGrid"%filename
	tg.write(outpath)




#parseFile("/Users/elias/Desktop/PartiturParsing/PD2/dlm/dlma5340.par,2")
regex = re.compile("[a-zA-Z0-9]+\.par,2")
end = "PD2"
if PD1:
	end = "PD1"
for directory in os.walk("/Users/elias/Desktop/PartiturParsing/"+end, topdown=True):
	for filename in directory[2]:
		#make sure it ends in .par,2
		m = re.match(regex,filename)
		if m is not None:
			#run the parseFile method
			parseFile(directory[0]+"/" +filename, filename)
			