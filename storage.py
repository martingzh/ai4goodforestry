from OCR_pipeline import extractTextFromPaper
import jsonpickle
# pip install -U jsonpickle


class PolicyPaper(object):
	country = []
	date = None
	title = []
	extractedText = []
	paperType = ""
	filename = ""

	# filename for now should be the relative path of the file
	def __init__ (self, filename):
		#(extracted text, (dates, [title candidates], countries))
		(et, mtd) = extractTextFromPaper(filename)
		self.country = mtd[2]
		self.date = mtd[0]
		self.title = mtd[1]
		self.extractedText = et
		# Currently paper type is a placeholder
		self.paperType = "policy"
		self.filename = filename
        


# def summary():


# A method that is used to convert Python Objects, i.e. PolicyPaper objects, to JSON files. 
# Argument: PolicyPaper instnace
# Return Value: True if stored, False otherwise.
# Stores files 

def serializeObject(paper, paper_name):
	json_object = jsonpickle.encode(paper)
	try:
		print(json_object,  file=open(paper_name, 'w'))
		return True
	except Exception as e:
		return False

# A method that is used to deserialize JSON objects and convert them into Python objects. 
# Argument: Filename (Relative Path)
# Return Value: Python object
def deserializeObject(filename):
	f = open(filename)
	js_string = f.read()
	thawed = jsonpickle.decode(js_string)
	f.close()
	return thawed


