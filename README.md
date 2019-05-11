# ai4goodforestry
A public repository used to demonstrate work done by our IEOR 135 project for AI For Good Foundation, with mentorship by James Hodson. This repository will seek to explore the relationship between NLP and forestry in policy documents.


## Installation 

### Prerequisite libraries to install: 

Pandas: `pip install pandas`

Numpy: `pip install numpy`

Jsonpickle: `pip install jsonpickle`

PDFMiner3: `pip install pdfminer3`

Geotext: `pip install geotext`

Gensim: `pip install gensim`

nltk: `pip install nltk`

Spacy: `pip install spacy`


### MySQL Database Setup 

To install the MySQL database, follow instructions from `MySQL Setup.ipynb`. 

## Relevant Directory and File Explanation

### Directories

`Policy PDFs`: Source document PDF's utilized, separated by subdirectories listed by country. 

`topic annotation`: Policy documents with the topics of each page tagged on the top left of each PDF. Instructions of how to tag documents by page are demonstrated by the `PDF with topics-per-page.ipynb` notebook.

`web app`: Contains our current work-in-progress infrastructure of the project. 

### Files

`Classification_Eng_Sp.ipynb`: Notebook used to predict a policy paper's incentives, disincentives, and motivations based on the frequency of keywords in a document. 

`MVP.ipynb`: Notebook used to demonstrate the functionality of text cleaning and extraction, Latent Dirichlet allocation (LDA) utilized on documents from India to generate topics, and visualization. 

`MySQL Setup.ipynb`: Notebook that gives instructions on how to set up the MySQL database. 

`Topic Modeling Pipeline Proof of Concept.ipynb`: Notebook that was used for testing purposes in deriving the appropriate model. Contributors are free to remove this notebook. 

`lda_model, lda_model.expElogbeta.npy, lda_model.id2word, lda_model.state`: An LDA model pretrained on policy documents from India. Used in conjunction with the function ```gensim.models.ldamodel.LdaModel.load("lda_model")```. 

`OCR_pipeline.py`: Library created to extract text from policy documents. 

`Sample-Data-Framework-Policy-Database.csv`: Annotations conducted by the partner team of Columbia students. 

`storage.py`: Library created to store policy papers as python objects, with functions to serialize and deserialize these objects. This library is currently not used much, but future contributors can take advantage of the opportunity of the `PolicyPaper` object to store both extracted text and metadata. 

`TopicModeling.py`: Contains the LDA modeling functionality. 


## Functionality

### Web App

This web app serves four purposes

 1. Extract text and information from policy paper PDFs
 2. Extract information about countries and their policies on a country level 
 3. Generate incentives, disincentives, and motivations per policy paper
 4. Add more policy papers to a database.

For the dynamic state, `cd` using the terminal into the `web app` directory and type `flask run`. 

For the static state, click on `home.html`.

The functionality of the web app is currently limited. 

### MySQL Database

Instructions for setting up the MySQL Database are in the `MySQL Setup.ipynb` notebook. 



### Document Tagging 

Functionality for how to tag documents by page are demonstrated in the `MVP.ipynb` notebook. Currently, the LDA model is trained on a sentence level from documents. From a high-level, the steps can be boiled down to as follows: 

1. Preprocess the text from policy papers and prepare a set of keywords and terms. 
2. Use functionality from the `TopicModeling.py` library to intialize and train the data. 
3. Manually label the topics generated from LDA and save this into a collection object. 
4. For each page in a new, unseen document, call `get_document_topics()` from `TopicModeling.py` to obtain the top three topics for a page. 




