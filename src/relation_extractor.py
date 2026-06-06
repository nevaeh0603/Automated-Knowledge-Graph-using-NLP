import spacy
nlp= spacy.load("en_core_web_sm")

def extract_relations(text):
    doc=nlp(text)
    triples=[]

    # Allowed relations
    valid_relations = ["found", "develop", "acquire", "work", "lead", "create", "build", "become"]

    for sent in doc.sents:
        subject=None
        relation=None
        object=None

        for token in sent:
            #Subject
            if token.dep_ == "nsubj":
                subject = token

            # Verb
            if token.pos_ == "VERB":
                verb = token.lemma_.lower()
                if verb in valid_relations:
                    relation = verb.upper()

            # Object
            if token.dep_ == "dobj":
                object = token

        if subject and relation and object:
            subject_text=" ".join([tok.text for tok in subject.subtree])
            object_text=" ".join([tok.text for tok in object.subtree])
            triples.append((subject_text, relation, object_text))

    triples = list(set(triples))            
    return triples