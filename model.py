'''
this module directly predicts whether a news is fake or not from a pretrained joblib file
find the actual model in this repository link : https://github.com/E-wave112/ml_proj_2/blob/master/fake_news_models.ipynb
'''

import joblib
import string
import warnings
warnings.filterwarnings('ignore')
import boto3
import sys
from decouple import config
import numpy as np
import pandas as pd
##extract punctuation marks from the string
import spacy
from spacy.util import minibatch, compounding
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split,KFold,cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,recall_score,precision_score,accuracy_score
from sklearn.pipeline import Pipeline
# from spacy.lang.en import English
##extract punctuation marks from the string
punctuations = string.punctuation
import dill

if sys.version_info[0] < 3: 
    from StringIO import StringIO # Python 2.x
    from BytesIO import BytesIO # Python 2.x
else:
    from io import StringIO,BytesIO # Python 3.x

##set your credentials and secret
AWS_ID = config('AWS_ID')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')

##use the boto3 sdk to integrate python and aws s3
client = boto3.client('s3', aws_access_key_id=AWS_ID,
        aws_secret_access_key=AWS_SECRET_KEY)

##get the object name and the object key(the actual .csv file)
bucket_name = 'edjangobucket'
object_key_joblib='fast.joblib'

joblib_load=client.get_object(Bucket=bucket_name,Key=object_key_joblib)

# def predict(text):
#     ##load the joblib pretrained model from s3
#     joblib_body=joblib_load['Body']
#     joblib_obj=joblib_body.read()
#     job_load_model=joblib.load(BytesIO(joblib_obj))
#     # args_array = np.array([title,text,subject])
#     text_predict=job_load_model.predict(text)
#     return text_predict

