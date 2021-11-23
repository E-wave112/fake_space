from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# declare the tokenizer object
max_words = 8192
tokenizer = Tokenizer(
    num_words = max_words,
    filters = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', 
    lower=True
)

MAX_SEQUENCE_LENGTH = 150
# helper function to tokenize inputs
def tokenize_texts(sentences:str):
    tokenizer.fit_on_texts(sentences)
    sentences = tokenizer.texts_to_sequences(sentences)
    sentences = pad_sequences(sentences,maxlen=MAX_SEQUENCE_LENGTH,padding='post')
    return sentences

