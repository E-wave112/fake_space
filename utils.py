import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# declare the tokenizer object
tokenizer = Tokenizer()

MAX_SEQUENCE_LENGTH = 150
# helper function to tokenize inputs
def tokenize_texts(sentences:str):
    tokenizer.fit_on_texts(sentences)
    token_seed = tokenizer.texts_to_sequences(sentences)
    token_seed_tensor = pad_sequences(token_seed,maxlen=MAX_SEQUENCE_LENGTH,padding='post')
    return token_seed_tensor

