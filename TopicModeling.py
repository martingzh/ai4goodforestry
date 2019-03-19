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

def lemmatization(nlp, texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=False)) 
              
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

#runs LDA on lemmatized text and returns corpus and LDA model
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