import spacy
nlp= spacy.load("en_core_web_md")

IGNORE_WORDS={"paper", "study", "research", "figure", "table", "section", "method", "result", "results", "approach", "using", "used", "this", "that", "these", "those", "which", "who", "whom", "whose", "it", "its", "they", "their"}

def preprocess(text):
    doc=nlp(text)
    clean_tokens=[]

    for token in doc:
        if not token.is_stop and not token.is_punct and token.text.lower() not in IGNORE_WORDS:
            clean_tokens.append(token.text)        #Removes stopwords and punctuations
    return " ".join(clean_tokens)