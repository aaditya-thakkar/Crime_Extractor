
# coding: utf-8

# In[1]:




# In[1]:




# In[1]:



# In[1]:




# In[1]:

import sys
print(sys.path)


# In[2]:

import os
import sys

#Set the correct environment variables
os.environ['SNORKELHOME']='/home/aaditya//Music/snorkel'
os.environ['PYTHONPATH']=':/home/aaditya/Music/snorkel:/home/aaditya/Music/snorkel/treedlib:/home/aaditya/Music/snorkel:/home/aaditya/Music/snorkel/treedlib'
os.environ['PATH']='/home/aaditya/bin:/home/aaditya/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/aaditya/Music/snorkel:/home/aaditya/Music/snorkel/treedlib:/home/aaditya/Music/snorkel:/home/aaditya/Music/snorkel/treedlib'

#Add python to the system path so that python can find the package
sys.path.append('/home/aaditya/Music/snorkel')
sys.path.append('/home/aaditya/Music/snorkel/treedlib')


# In[3]:

get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')
get_ipython().magic(u'matplotlib inline')
import os

# TO USE A DATABASE OTHER THAN SQLITE, USE THIS LINE
# Note that this is necessary for parallel execution amongst other things...
# os.environ['SNORKELDB'] = 'postgres:///snorkel-intro'

from snorkel import SnorkelSession
session = SnorkelSession()
# Here, we just set a global variable related to automatic testing- you can safely ignore this!
max_docs = 50 if 'CI' in os.environ else float('inf')


# In[4]:

from snorkel.parser import TSVDocPreprocessor

doc_preprocessor = TSVDocPreprocessor('tutorials/intro/data/articles.tsv', max_docs=max_docs)


# In[5]:

from snorkel.parser import CorpusParser

corpus_parser = CorpusParser()
get_ipython().magic(u'time corpus_parser.apply(doc_preprocessor)')


# In[6]:

from snorkel.models import Document, Sentence

print "Documents:", session.query(Document).count()
print "Sentences:", session.query(Sentence).count()

dict_final={}

crimetype_murder=['killed','kill', 'kills', 'killing', 'murder', 'shot', 'shooting','convicted','murdered']
crimetype_rape=['rape', 'raped', 'gangraped', 'molested', 'molestation', 'molesting', 'harassment', 'raping']
crimetype_attack=['hurt','rioting' ,'injured','attack','beating up','attacked']
crimetype_impersonation=["impersonator","impersonation","impersonating"]
date=''
for doc in session.query(Document).all():
    crimetype=""
    date=''
    for i,sent in enumerate(doc.sentences):
        if(i==0):
            date=str(sent.text[0:10])
        sent_text= sent.text.lower()
        for x in crimetype_murder:
            if (x in sent_text):
                crimetype = 'Murder'
                break
        if(crimetype==""):
            for x in crimetype_rape:
                if (x in sent_text):
                    crimetype = 'Sexual Assault'
                    break
        if(crimetype==""):    
            for x in crimetype_attack:
                if (x in sent_text and crimetype==""):
                    crimetype = 'Attack'
                    break
                
        if ((("kidnapped" in sent_text) or ("kidnapping" in sent_text)) and crimetype==""):
            crimetype = 'kidnapping'
            break
        if (("suicide" in sent_text) and crimetype==""):
            crimetype = 'Suicide'
            break
        if (("cyber" in sent_text) and ("crime" in sent_text) and crimetype==""):
            crimetype = 'Cyber Crime'
            break
        if(crimetype==""):    
            for x in crimetype_impersonation:
                if (x in sent_text and crimetype==""):
                    crimetype = 'Impersonation'
                    break
        if (("drug" in sent_text) and ("drugs" in sent_text) and crimetype==""):
            crimetype = 'Drugs related Crime'
            break
    print(doc, date, crimetype)
    dict_final[doc] = {'docno': doc,
                      'date' : date,
                      'crimetype' : crimetype,
                      'location': []}

# In[2]:

# In[7]:

from snorkel.models import candidate_subclass
LocationPer = candidate_subclass('LocationPer', ['location', 'person'])
# Location = candidate_subclass('Location', ['location'])

# In[8]:

from snorkel.candidates import Ngrams, CandidateExtractor
from snorkel.matchers import PersonMatcher, LocationMatcher

ngrams         = Ngrams(n_max=3)
person_matcher = PersonMatcher(longest_match_only=True)
location_matcher = LocationMatcher(longest_match_only=True)
cand_extractor = CandidateExtractor(LocationPer, 
                                    [ngrams, ngrams], [person_matcher, location_matcher],
                                    symmetric_relations=False)

# cand_extractor2 = CandidateExtractor(Location, 
#                                     [ngrams], [location_matcher],
#                                     symmetric_relations=False)

# In[9]:

def number_of_people(sentence):
    active_sequence = False
    count = 0
    for tag in sentence.ner_tags:
        if tag == 'LOCATION' and not active_sequence:
            active_sequence = True
            count += 1
        elif tag != 'LOCATION' and active_sequence:
            active_sequence = False
    return count


# In[11]:

from snorkel.models import Document

docs = session.query(Document).order_by(Document.name).all()
ld   = len(docs)
# count = 0
train_sents = set()
dev_sents   = set()
test_sents  = set()
splits = (0.9, 0.95) if 'CI' in os.environ else (0.9, 0.95)
for i,doc in enumerate(docs):
    for s in doc.sentences:
        if number_of_people(s) < 15:
#             count+=1
            if i < splits[0] * ld:
                train_sents.add(s)
            elif i < splits[1] * ld:
                dev_sents.add(s)
            else:
                test_sents.add(s)
# print count


# In[3]:

get_ipython().magic(u'time cand_extractor.apply(train_sents, split=0)')

# In[16]:

train_cands = session.query(LocationPer).filter(LocationPer.split == 0).all()
print "Number of candidates:", len(train_cands)


# In[17]:

print train_cands


import re
import numpy as np
from snorkel.lf_helpers import (
    get_left_tokens, get_right_tokens, get_between_tokens,
    get_text_between, get_tagged_text,
)

import re
import numpy as np
from snorkel.lf_helpers import (
    get_left_tokens, get_right_tokens, get_between_tokens,
    get_text_between, get_tagged_text,
)

crime_tags = {'killed','kill', 'kills', 'killing', 'kidnapped','kidnapping','shooting','convicted','murdered','attack','beating up','fraud','attacked','murder', 'rape', 'raped', 'assulated', 'imprisoned','accused', 'hanging', 'hanged', 'gangraped', 'died', 'hurt','rioting' ,'injured', 'shot','intimidation', 'suicide', 'molested', 'molesting', 'death', 'jailed'}
police_tags = {'Police','police','police station'}
vic_tags = {'victim'}

def LF_crime_detect(c):
    return 1 if len(crime_tags.intersection(get_between_tokens(c))) > 0 else 0

def LF_location_left_window(c):
    if len(crime_tags.intersection(get_left_tokens(c[1], window=7))) > 0:
        return 1
    else:
        return 0

def LF_location_left_per_vic_window(c):
    if len(vic_tags.intersection(get_left_tokens(c[0], window=7))) > 0:
        return 1
    else:
        return 0
def LF_police_at_location_left(c):
    if len(police_tags.intersection(get_right_tokens(c[1], window=7))) > 0:
        return 1
    else:
        return 0
    
    
LFs = [
    LF_crime_detect, LF_location_left_window, LF_police_at_location_left, LF_location_left_per_vic_window
]


from snorkel.annotations import LabelAnnotator
labeler1 = LabelAnnotator(f=LFs)

np.random.seed(1701)
get_ipython().magic(u'time L_train = labeler1.apply(split=0)')
L_train


L_train = labeler1.load_matrix(session, split=0)
L_train

for docno in session.query(Document).all():
    print(docno)
    for i in range(L_train.shape[0]):
        if(L_train[i,:].toarray()[0][0] == 1.0):
            if(session.query(LocationPer).filter(LocationPer.split == 0)[i].get_parent().get_parent()==docno):
                print(session.query(LocationPer).filter(LocationPer.split == 0)[i])


# In[3]:
import json
for docno in session.query(Document).all():
    print(docno)
    for i in range(L_train.shape[0]):
        if(L_train[i,:].toarray()[0][0] == 1.0):
            if(session.query(LocationPer).filter(LocationPer.split == 0)[i].get_parent().get_parent()==docno):
                print(session.query(LocationPer).filter(LocationPer.split == 0)[i][1].get_span())
                dict_final[docno]['location'].append(json.dumps(session.query(LocationPer).filter(LocationPer.split == 0)[i][1].get_span()))


# In[ ]:

print(dict_final)


# In[ ]:



