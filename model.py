import os
import re
import string
import warnings
warnings.filterwarnings('ignore')
import boto3
import pandas as pd
import sys
import spacy
from decouple import config
from spacy.util import minibatch, compounding
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split,KFold,cross_val_score
from sklearn.ensemble import RandomForestClassifier
##extract punctuation marks from the string
punctuations = string.punctuation

if sys.version_info[0] < 3: 
    from StringIO import StringIO # Python 2.x
else:
    from io import StringIO # Python 3.x

##set your credentials and secret
AWS_ID = config('AWS_ID')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')

##use the boto3 sdk to integrate python and aws s3

client = boto3.client('s3', aws_access_key_id=AWS_ID,
        aws_secret_access_key=AWS_SECRET_KEY)

##get the object name and the object key(the actual .csv file)
bucket_name = 'edjangobucket'
object_key = 'fake_news.csv'

csv_object = client.get_object(Bucket=bucket_name, Key=object_key)
csv_body = csv_object['Body']
csv_string = csv_body.read().decode('utf-8')

df = pd.read_csv(StringIO(csv_string))
##drop the date column
df.drop(['date'],axis=1,inplace=True)
##print the head and shape of the data
print(df.info())
##load the english nlp pipeline
spacy_eng_token = spacy.load('en_core_web_sm')

##data cleansing and preprocessing
##tokenize the words
def tokenize(text):
    return spacy_eng_token(text)
#remove stop words
def remove_stop(text):
    return ''.join([word for word in text if word.is_stop==False])


data_process = df[['title','text','subject']]
##apply the above helper functions
# Creating our tokenizer function
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    tokens = spacy_eng_token(sentence)

    # Lemmatizing each token and converting each token into lowercase
    tokens_list = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens ]

    # Removing stop words
    mytokens = [ word for word in tokens_list if word not in STOP_WORDS and word not in punctuations ]

    # return preprocessed list of tokens
    return mytokens

# Custom transformer using spaCy
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [clean_text(text) for text in X],[remove_nums(text) for text in X],[remove_nicks_symbols(text) for text in X],[remove_url(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}

# Basic function to clean the text
def clean_text(text):
    # Removing spaces and converting text into lowercase
    return text.strip().lower()
##remove numbers/digits
def remove_nums(text):
    return ''.join([word for word in text if not word.isdigit()])

def remove_nicks_symbols(text):
    return re.sub(r"\@\S+", "",text)

##remove urls
def remove_url(text):
    # url = re.compile(r'https?://\S+|www\.\S+')
    return re.sub(r'https?://\S+|www\.\S+',"", text)


##create a vectorizer from the bag of words matrix for our texts
bow_vector = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1))

##apply these functions to the dataset
data_process.applymap(lambda x:spacy_tokenizer(x))
data_process.apply(lambda x:clean_text(x))
data_process.apply(lambda x:remove_nums(x))
data_process.apply(lambda x:remove_nicks_symbols(x))
data_process.apply(lambda x:remove_url(x))
print(data_process.head())

X=data_process
y=df['Type']

rnd_clf = RandomForestClassifier()
cv = KFold(n_splits=5, random_state=42, shuffle=True)

##perform kfold cv
print('preparing to split')
for train_index,test_index in cv.split(X):
    print('split started')
    print(train_index,test_index)
    X_train,X_test,y_train,y_test = X.iloc[train_index],X.iloc[test_index],y.iloc[train_index],y.iloc[test_index]
    rnd_clf.fit(X_train, y_train)
    print(cross_val_score(rnd_clf, X, Y, cv=5))



# X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,shuffle=True,random_state=10)


