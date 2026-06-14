import spacy
nlp= spacy.load("en_core_web_lg")

def preprocess(text):
    doc=nlp(text)
    clean_tokens=[]

    for token in doc:
        if not token.is_stop and not token.is_punct:
            clean_tokens.append(token.text)        #Removes stopwords and punctuations

    return " ".join(clean_tokens)