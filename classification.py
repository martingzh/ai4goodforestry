import OCR_pipeline as OCR
import TopicModeling as TM
import jsonpickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

#import the data from mySQL database
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="XXX", #Please replace this with your own mySQL password
  database="forestry"
)
mycursor = mydb.cursor()

def getExtractedTexts():
    mycursor.execute("SELECT filename, extractedText FROM PolicyPapers")
    myresult = mycursor.fetchall()
    return [x for x in myresult]

def getExtractedTextsFromCountries(countries):
    sqlStatement = "SELECT filename, extractedText FROM PolicyPapers WHERE"
    
    for i in range(len(countries)):
        whereClause = " country = '%s' " % countries[i]
        sqlStatement += whereClause
        if len(countries) != 1 and i < len(countries) - 1:
            sqlStatement += "or"
            
    mycursor.execute(sqlStatement)
    myresult = mycursor.fetchall()
    return [x for x in myresult]

#Extract text files 
import re
import gc
textDictionary = {}

India = getExtractedTextsFromCountries(['India'])
Brazil = getExtractedTextsFromCountries(['Brazil'])
Mexico = getExtractedTextsFromCountries(['Mexico'])

IndiaPapers = {}
BrazilPapers = {}
MexicoPapers = {}

for paper in India:
    IndiaPapers.update({paper[0].replace('.pdf','') : re.sub(r'(.) ', r'\1', paper[1])})

for paper in Brazil:
    BrazilPapers.update({paper[0].replace('.pdf','') : re.sub(r'(.) ', r'\1', paper[1])})

for paper in Mexico:
    MexicoPapers.update({paper[0].replace('.pdf','') : re.sub(r'(.) ', r'\1', paper[1])})

#Convert to DataFrames
India_df = pd.Series(IndiaPapers).to_frame()
Brazil_df = pd.Series(BrazilPapers).to_frame()
Mexico_df = pd.Series(MexicoPapers).to_frame()

#Import labeled data
df = pd.read_csv('Sample Data Framework - Policy Database.csv')
df = df.drop(index=0)

#English(India)
Eng_key_words = ['afforestation','agriculture','animal welfare','artificial regeneration','biodiversity',
             'biological resources','biome','board','clean','coconut','conservation','control','database',
             'enforcement','environment','farm','financing','forest','forest protection','funding','fundraising',
             'land ','land use','landholder','law','measuring','mobilization','monitor','natural resources',
             'oversight','plant breeders','plants','pollution','preservation','produce','protection','qualification',
             'quality','registry','regulation','reporting','reserve','resource','restriction','results-driven',
             'rural','safeguard','species' ,'support','sustainable','technical submission','threatened species',
             'variety','verification','wastewater','water','watershed','wild life']

#Add keyword columns with each entry its frequency
for word in Eng_key_words:
    India_df[word] = np.zeros(len(India_df))
    for i in range(len(India_df)):
        India_df[word][i] = India_df[0][i].count(word)

#Data cleaning
India_df = India_df.drop(index=['_MineralConservationandDevelopmentRules1988-converted'])
just_india = df[df['Country'] == 'IN'][['Policy Title','Primary Incentive...','Primary Disincentive...','Motivation']]
india_reordered = just_india.iloc[[7,17,9,4,2,3,0,20,1,12,14,8,18,19,13,5,11,15,16],:]
india_reordered = india_reordered.reset_index().drop(columns = 'index')
India_df = India_df[Eng_key_words].reset_index().drop(columns='index')

#Spanish(Mexico)
spanish_key_words = ['repoblación forestal', 'agricultura', 'bienestar de los animales', 'regeneración artificial', 
                     'biodiversidad', 'recursos biologicos', 'bioma', 'tablero', 'limpiar', 'Coco', 'conservación',
                     'controlar', 'base de datos', 'aplicación', 'ambiente', 'granja', 'financiación', 'bosque', 
                     'protección forestal', 'fondos', 'recaudación de fondos', 'tierra', 'uso del suelo', 
                     'terrateniente', 'ley', 'medición', 'movilización', 'monitor', 'recursos naturales', 'vigilancia',
                     'fitomejoradores', 'plantas', 'contaminación', 'preservación', 'Produce', 'proteccion',
                     'calificación', 'calidad', 'registro', 'regulación', 'reportando', 'reserva', 'recurso', 
                     'restricción', 'impulsado por resultados', 'rural', 'salvaguardia', 'especies', 'apoyo', 
                     'sostenible', 'sumisión técnica', 'especies amenazadas', 'variedad', 'verificación', 
                     'aguas residuales', 'agua', 'cuenca', 'fauna silvestre']

#Add keyword columns with each entry its frequency
for word in spanish_key_words:
    Mexico_df[word] = np.zeros(len(Mexico_df))
    for i in range(len(Mexico_df)):
        Mexico_df[word][i] = Mexico_df[0][i].count(word)

#Data Cleaning
Mexico_df = Mexico_df.drop(index=['Mexico Forestry Law'])
just_mexico = df[df['Country'] == 'MX'][['Policy Title','Primary Incentive...','Primary Disincentive...','Motivation']].reset_index().drop(columns=['index'])
mexico_reordered = just_mexico.iloc[[6,10,16,5,13,21,17,8,22,2,1,12,9,20,14,23,15,19,7,3,4,18,24,11],:]
mexico_reordered = mexico_reordered.reset_index().drop(columns = 'index')
Mexico_df = Mexico_df[spanish_key_words].reset_index().drop(columns='index')

#Define a classification function
#Auguments:
#document=long string
#classify_india = True if the document is from India
#classify_mexico = True if predicting Mexico
# is_incentive = True if predicting incentive 
# is_disincentive True if predicting disincentive
# is_motivation True if predicting motivation
#Return:
#incentive/disincentive/motivation
def Classify(document,classify_india,classify_mexico,is_incentive,is_disincentive,is_motivation)
	doc_df = pd.Series(document).to_frame()
	for word in Eng_key_words:
	    doc_df[word][0] = doc_df[0][0].count(word)

	if classify_india:
		incentives = ['Diplomatic','Financial-grants','Financial-subsidies','Fianncial-trade','Legal']
		disincentives = ['Financial-fines', 'Imprisonment and Fines', 'Procesures/Guidelines']
		motivations = ['Agricultural Development','Climate Change Action','Conservation','International Agreement/Conference','Previous Supreme Court Ruling']

		#Models
		#Incentive:
		if is_incentive:
			X = India_df
			y = india_reordered['Primary Incentive...'].astype('category').cat.codes

			X = X.drop(index=y[y==-1].index)
			y = y.drop(index=y[y==-1].index)

			rf = RandomForestClassifier(n_estimators=100, random_state=0)
			rf.fit(X, y)
			return(incentives[rf.predict(doc_df[Eng_key_words].values.reshape(1,-1))[0]])
		#Disincentive:
		if is_disincentive:
			X = India_df
			y = india_reordered['Primary Disincentive...'].astype('category').cat.codes

			X = X.drop(index=y[y==-1].index)
			y = y.drop(index=y[y==-1].index)

			rf = RandomForestClassifier(n_estimators=100, random_state=0)
			rf.fit(X, y)
			return(disincentives[rf.predict(doc_df[Eng_key_words].values.reshape(1,-1))[0]])
		if is_motivation:
			X = India_df
			y = india_reordered['Motivation'].astype('category').cat.codes

			X = X.drop(index=y[y==-1].index)
			y = y.drop(index=y[y==-1].index)

			rf = RandomForestClassifier(n_estimators=100, random_state=0)
			rf.fit(X, y)	
			return (motivations[rf.predict(doc_df[Eng_key_words].values.reshape(1,-1))[0]])

	if classify_mexico:
		incentives = ['Diplomatic','Financial-grants','Financial-subsidies','Fianncial-tax break','Legal','Political']
		disincentives = ['Financial-fines', 'Financial-fines, Legal, Imprisonment and Fines', 'Financial-fines, Legal, Political', 'Procedures/Guidelines']
		motivations = ['Agricultural Development','Climate Change Action','Conservation','International Agreement/Conference']

		if is_incentive:
			X = Mexico_df
			y = mexico_reordered['Primary Incentive...'].astype('category').cat.codes

			X = X.drop(index=y[y==-1].index)
			y = y.drop(index=y[y==-1].index)

			rf = RandomForestClassifier(n_estimators=100, random_state=0)
			rf.fit(X, y)
			return(incentives[rf.predict(doc_df[spanish_key_words].values.reshape(1,-1))[0]])

		if is_disincentive:
			X = Mexico_df
			y = mexico_reordered['Primary Disincentive...'].astype('category').cat.codes

			X = X.drop(index=y[y==-1].index)
			y = y.drop(index=y[y==-1].index)

			rf = RandomForestClassifier(n_estimators=100, random_state=0)
			rf.fit(X, y)
			return(disincentives[rf.predict(doc_df[spanish_key_words].values.reshape(1,-1))[0]])

		if is_motivation:
			X = Mexico_df
			y = mexico_reordered['Motivation'].astype('category').cat.codes

			X = X.drop(index=y[y==-1].index)
			y = y.drop(index=y[y==-1].index)

			rf = RandomForestClassifier(n_estimators=100, random_state=0)
			rf.fit(X, y)
			return(motivations[rf.predict(doc_df[spanish_key_words].values.reshape(1,-1))[0]])










