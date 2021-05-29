import re
from sklearn.base import TransformerMixin
# Basic function to clean the text
def clean_text(text):
    ##remove numbers
    text_nums=''.join([word for word in text if not word.isdigit()])
    ##remove urls
    text_urls= re.sub(r'https?://\S+|www\.\S+',"", text_nums)
    ##remove nicks
    text_nicks= re.sub(r"\@\S+", "",text_urls)
    # Removing spaces and converting text into lowercase
    return text_nicks.strip().lower()

# define a custom transformer fo our spacy model
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [clean_text(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}