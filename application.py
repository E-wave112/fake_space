import os
import warnings
warnings.filterwarnings('ignore')
import boto3
import pandas as pd
import sys
from decouple import config

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
##print the head and shape of the data
print(df.head())
print(df.shape)