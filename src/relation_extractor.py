import spacy
nlp = spacy.load("en_core_web_sm")

def extract_relations(text):
    doc = nlp(text)
    triples = []
    valid_relations = ["found","develop","acquire","work","lead","create", "build","become"]

    for sent in doc.sents:
        subject = None
        relation = None
        object_ = None

        for token in sent:
            # Subject
            if token.dep_ == "nsubj":
                subject = token

            # Verb
            if token.pos_ == "VERB":
                verb = token.lemma_.lower()
                if verb in valid_relations:
                    relation = verb.upper()

            # Object
            if token.dep_ == "dobj":
                object_ = token

        if subject and relation and object_:
            subject_text = " ".join([tok.text for tok in subject.subtree])
            object_text = " ".join([tok.text for tok in object_.subtree])
            triples.append((subject_text, relation, object_text))

    return list(set(triples))

def custom_relations(text):
    triples = []
    doc = nlp(text)
    for sent in doc.sents:
        sentence = sent.text.lower()

        if "founded" in sentence and "founded by" not in sentence:
            founder = None
            company = None
            for token in sent:
                if token.dep_ == "nsubj":
                    founder = " ".join([tok.text for tok in token.subtree])

                if token.dep_ == "dobj":
                    company = " ".join([tok.text for tok in token.subtree])

            if founder and company:
                triples.append((founder, "FOUNDED", company))

        if "founded by" in sentence:
            entities = [(ent.text, ent.label_)for ent in sent.ents]
            company = None
            for ent_text, ent_label in entities:
                if ent_label == "ORG":
                    company = ent_text
                    break
            founders = [ent_text  for ent_text, ent_label in entities  if ent_label == "PERSON"]

            if company:
                for founder in founders:
                    triples.append((founder, "FOUNDED", company) )

        if ( "ceo of" in sentence or "chief executive officer" in sentence):
            entities = [(ent.text, ent.label_)for ent in sent.ents]
            persons = [e[0] for e in entities if e[1] == "PERSON"]
            orgs = [ e[0] for e in entities if e[1] == "ORG"]
            for person in persons:
                for org in orgs:
                    triples.append( (person, "CEO_OF", org))

        if "works at" in sentence:
            entities = [(ent.text, ent.label_) for ent in sent.ents]
            persons = [e[0] for e in entities if e[1] == "PERSON"]
            orgs = [e[0] for e in entities if e[1] == "ORG"]
            for person in persons:
                for org in orgs:
                    triples.append((person, "WORKS_AT", org))

        if ( "located in" in sentence or "headquartered in" in sentence):
            entities = [(ent.text, ent.label_) for ent in sent.ents]
            orgs = [e[0] for e in entities if e[1] == "ORG" ]
            locations = [e[0] for e in entities if e[1] in ["GPE", "LOC"]]

            if len(orgs) > 0:
                for org in orgs:
                    for location in locations:
                        triples.append((org, "LOCATED_IN", location))

            else:
                company = sent.text.split()[0]
                for location in locations:
                    triples.append((company, "LOCATED_IN", location))

    return list(set(triples))