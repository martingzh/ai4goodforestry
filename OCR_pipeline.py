# A library that contains the methods used for OCR extraction. Note, this library is specific to the directory
# structure of "sample data" in the ai4goodforestry github. 
# Note: This notebook specifically only cares about extracting policy papers and its relevant information.
# For other data such as statistics, use another library. 

import PIL
from wand.image import Image
import pytesseract
import cv2
import os
import numpy as np
import io

# A method that extracts text from the PDF. Please supply relative path of PDF
# Argument: filename relative path (i.e. "sample data/Kenya/AgricultureFisheriesandFoodAuthorityNo13of2013.PDF")
# Returns: A python list where each element of the list 
# contains the contents corresponding to one page of the file
# Note: This might take a while to run.

def extractTextFromPaper(filename):
	# Convert a PDF into a form that we can utilize the wand library
	image_pdf = Image(filename=filename, resolution=300)
	# Convert this to JPEG so that we can extract information that we can feed into pytesseract
	image_jpeg = image_pdf.convert('jpeg')
	image = []
	final_text = []
	# Convert the images on each page to blobs (binary strings)
	for img in image_jpeg.sequence:
	    img_page = Image(image=img)
	    image.append(img_page.make_blob('jpeg'))
	print("Images converted to binary strings")
	# Extract text
	for img in image:
	    text = pytesseract.image_to_string(PIL.Image.open(io.BytesIO(img)))
	    final_text.append(text)
	print("Paper successfully converted!")
	return final_text

# A method that extracts all the text from a specific folder in sample data. 
# Argument: Folder that you want to extract text from
# Returns: A dictionary where the key-value relationship is "File Name":"Python list of contents"
# Note: If you change how the papers are structured, you will need to modify this code
# Note: This might take a while to run.

def extractTextFromAllPapers(foldername):
	pretext = "sample data/"
	directory_path = pretext + foldername
	# Retrieve file names inside folder
	files = os.listdir(directory_path)
	print("File now open.")
	# Create a dictionary where we map files names to OCR extracted text
	country_papers = {}
	for file in files:
		contents = extractTextFromPaper(file)
		country_papers[file] = contents
	return country_papers

# A method to extract metadata from a specific policy paper. 
# Arguments: filename is the file name of the relevant policy paper

def extractMetaData(filename, extractedText):

	return

