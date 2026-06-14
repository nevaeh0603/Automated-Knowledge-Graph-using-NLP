import spacy
nlp = spacy.load("en_core_web_lg")
def extract_entities(text):
    doc = nlp(text)
    entities = []
    important_labels = ["PERSON", "ORG", "GPE", "DATE","MONEY"]

    for ent in doc.ents:
        if ent.label_ in important_labels:
            entities.append((ent.text, ent.label_))
    return entities

def remove_duplicates(entities):
    unique_entities = []

    for ent in entities:
        if ent not in unique_entities:
            unique_entities.append(ent)

    return unique_entities