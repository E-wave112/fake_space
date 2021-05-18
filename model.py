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
##extract punctuation marks from the string
punctuations = string.punctuation

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

def predict(text):
    ##load the joblib pretrained model from s3
    joblib_body=joblib_load['Body']
    joblib_obj=joblib_body.read()
    job_load_model=joblib.load(BytesIO(joblib_obj))
    text_predict=job_load_model.predict(text)
    return text_predict

