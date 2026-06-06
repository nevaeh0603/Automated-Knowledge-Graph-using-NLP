import spacy
nlp= spacy.load("en_core_web_sm")

def extract_relations(text):
    doc=nlp(text)
    relation=[]

    for sent in doc.sents:
        subject=None
        relation=None
        object=None

        for token in sent:
            #Subject
            if token.dep_ == "nsubj":
                subject = token.text

            # Verb
            if token.pos_ == "VERB":
                relation = token.lemma_

            # Object
            if token.dep_ in ["dobj", "pobj"]:
                object_ = token.text

        if subject and relation and object_:
            relation.append((subject, relation, object_))
            
    return relation