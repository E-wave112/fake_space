'''
this module directly predicts whether a news is fake or not from a pretrained joblib file
find the actual model in this repository link : https://github.com/E-wave112/ml_proj1/blob/master/aws_nlp.ipynb
'''
import tempfile
import warnings
warnings.filterwarnings('ignore')
from decouple import config
import numpy as np
    


AWS_ID = config('AWS_ID')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')

# create a helper function for accessing our cloud based s3 filesystem
BUCKET_NAME="edjangobucket"


def get_aws3_fs():
  return s3fs.S3FileSystem(key=AWS_ID,secret=AWS_SECRET_KEY)


# def predict(title,text,subject):
#     args_array = np.array([title,text,subject])
#     text_predict=job_load_model.predict(args_array)
#     return text_predict

