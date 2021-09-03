'''
this module directly predicts whether a news is fake or not from a pretrained joblib file
find the actual model in this repository link : https://github.com/E-wave112/ml_proj1/blob/master/aws_nlp.ipynb
'''

import joblib
import warnings
warnings.filterwarnings('ignore')
import boto3
import sys
from decouple import config

if sys.version_info[0] < 3: 
    from StringIO import StringIO # Python 2.x
    from BytesIO import BytesIO # Python 2.x
else:
    from io import StringIO,BytesIO # Python 3.x


AWS_ID = config('AWS_ID')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')

##use the boto3 sdk to integrate python and aws s3
client = boto3.client('s3', aws_access_key_id=AWS_ID,
        aws_secret_access_key=AWS_SECRET_KEY)

##get the object name and the object key(the actual .joblib file)
bucket_name = 'edjangobucket'
object_key_joblib='nlp_model.h5'
joblib_load=client.get_object(Bucket=bucket_name,Key=object_key_joblib)
##load the joblib pretrained model from s3
joblib_body=joblib_load['Body']
joblib_obj=joblib_body.read()
job_load_model=joblib.load(BytesIO(joblib_obj))


def predict(title,text,subject):
    ##load the joblib pretrained model from s3
    # joblib_body=joblib_load['Body']
    # joblib_obj=joblib_body.read()
    # job_load_model=joblib.load(BytesIO(joblib_obj))
    args_array = np.array([title,text,subject])
    text_predict=job_load_model.predict(args_array)
    return text_predict

