from OCR_pipeline import extractTextFromPaper
import jsonpickle
# pip install -U jsonpickle


# A class that stores relevant metadata and text from a specific policy paper
class PolicyPaper(object):
	# Class Variables
	country = []
	date = None
	title = []
	extractedText = []
	paperType = ""
	filename = ""
	cleanedText = None
	LDA = None
	corpus = None

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
# A method to retrieve file name by passing in the file path
# Returns a file name

def getFileName(file_path):
	file_name = file_path.rsplit('/', 1)[1]
	dot_index = file_name.rfind('.')
	if dot_index == -1:
		return file_name
	return file_name[:dot_index]

# A method that is used to convert Python Objects, i.e. PolicyPaper objects, to JSON files. 
# Argument: PolicyPaper instnace
# Return Value: True if stored, False otherwise.
# Stores files 

def serializeObject(paper):
	json_object = jsonpickle.encode(paper)
	paper_name = "object storage/" + getFileName(paper.filename) + ".txt"   
	try:
		print(json_object,  file=open(paper_name, 'w'))
		return paper_name
	except Exception as e:
		return None

# A method that is used to deserialize JSON objects and convert them into Python objects. 
# Argument: Filename (Relative Path)
# Return Value: Python object
def deserializeObject(filename):
	f = open(filename)
	js_string = f.read()
	thawed = jsonpickle.decode(js_string)
	f.close()
	return thawed


