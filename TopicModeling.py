#A library for extracting topic models from text files. To extract text, use methods from OCR_pipeline.py

import gensim
import nltk
import spacy
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
nltk.download('punkt')

#def make_bigrams(texts):
 #   return [bigram_mod[doc] for doc in texts]

#def make_trigrams(texts):
#    return [trigram_mod[bigram_mod[doc]] for doc in texts]


#A method to lemmatize a list of texts
#Arguments:
#nlp: spacy model to be used
#texts: list of texts to be lemmatized
#allowed_postags: allowed parts of speech for lemmatized text
#Returns: list of lemmatized texts 

def lemmatization(nlp, texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out



#A method to convert a list of sentences into a list of words
#Arguments: the list of sentences to be processed
#Returns: a list of words

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=False)) 

        
        
#A method to convert a list of pages into a list of sentences
#Arguments: list of pages
#Returns: list of lemmatized sentences

def toSentences(pageList):    
    # convert into long string (from list of page texts)
    longString = ''.join(pageList).replace('\n',' ')
    # split into list of sentences
    sentences = nltk.sent_tokenize(longString)
        
    # Remove Stop Words
    # sentences_nostops = remove_stopwords(sentences)
    
    # Convert sentences to list of words
    data_words = list(sent_to_words(sentences))
    
    # Form Bigrams
    #sentences_bigrams = make_bigrams(data_words)
    sentences_bigrams = data_words

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en
    nlp = spacy.load('en', disable=['parser', 'ner'])
    sentences_lemmatized = lemmatization(nlp, sentences_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    
    return sentences_lemmatized



#A method that runs LDA on lemmatized text and returns corpus and LDA model
#Arguments: list of lemmatized sents
#Returns: list containing corpus and lda model

def LDA(lemmatized_sents):
    #create dictionary
    id2word = corpora.Dictionary(lemmatized_sents)
    
    # Creates corpus
    corpus = [id2word.doc2bow(lemmatized_sent) for lemmatized_sent in lemmatized_sents]
    
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=30, 
                                           random_state=100,
                                           update_every=3,
                                           passes=30,
                                           alpha='auto',
                                           per_word_topics=True)
    
    return [corpus, lda_model]

def pull_sentences_with_keywords(sentences, keywords):
    sentences_out = []
    
    for sentence in sentences:
        if set(sentence).intersection(set(keywords)) != set(sentence):
            sentences_out.append(sentence)
            
    return sentences_out







