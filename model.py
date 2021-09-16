'''
this module directly predicts whether a news is fake or not from a pretrained joblib file
find the actual model in this repository link : https://github.com/E-wave112/ml_proj1/blob/master/aws_nlp.ipynb
'''
import tempfile
import warnings
warnings.filterwarnings('ignore')
from decouple import config
import numpy as np
import s3fs
import keras
    


AWS_ID = config('AWS_ID')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')

# create a helper function for accessing our cloud based s3 filesystem
BUCKET_NAME="edjangobucket"

def get_aws3_fs():
  return s3fs.S3FileSystem(key=AWS_ID,secret=AWS_SECRET_KEY)


# helper function to load our model from s3
def s3_load_keras_model(model_name: str):
      with tempfile.TemporaryDirectory() as tempdir:
        s3fs = get_aws3_fs()
        # Fetch and save the zip file to the temporary directory
        s3fs.get(f"{BUCKET_NAME}/{model_name}.h5", f"{tempdir}/{model_name}.h5")
        # Load the keras model from the temporary directory
        return keras.models.load_model(f"{tempdir}/{model_name}.h5")


# predictor helper function
def predict(args_dict:dict):
    # args_array = np.array([title,text,subject])
    loaded_model = s3_load_keras_model("nlp_model")
    text_predict=loaded_model.predict(args_dict)
    return text_predict


