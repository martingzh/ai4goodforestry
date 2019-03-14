from OCR_pipeline import extractTextFromPaper

class storeObject(object):
	paper = ""

class PolicyPaper(object):
	country = []
	date = None
	title = []
	extractedText = []
	paperType = ""

def __init__ (self, filename):
	#(extracted text, (dates, [title candidates], countries))
	(et, mtd) = extractTextFromPaper(filename)
	self.country = mtd[2]
	self.date = mtd[0]
	self.title = mtd[1]
	self.extractedText = et
	paperType = "policy"

# def summary():

