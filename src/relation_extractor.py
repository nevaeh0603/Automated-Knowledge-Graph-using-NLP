import spacy
import re
nlp = spacy.load("en_core_web_md")

IGNORE_WORDS={"paper", "study", "research", "figure", "table", "section", "method", "result", "results", "approach", "using", "used", "this", "that", "these", "those", "which", "who", "whom", "whose", "it", "its", "they", "their"}

def extract_relations(text):
    doc = nlp(text)
    triples = []
    stop_verbs = ["be", "have", "do"]

    for sent in doc.sents:
        #Skip citations
        if "et al" in sent.text.lower():
            continue

        subject = None
        relation = None
        object = None

        for token in sent:
            # Subject
            if token.dep_ in ["nsubj", "nsubjpass"]:
                subject = token

            # Verb
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                verb = token.lemma_.lower()
                if verb not in stop_verbs:
                    relation = re.sub(r'[^A-Za-z0-9_]', '_', verb.upper())
                    if len(relation) < 2:
                        continue

            # Object
            if (token.dep_ in ["dobj", "pobj", "attr"] and token.pos_ in ["NOUN", "PROPN"]):
                object = token

        if subject and relation and object:
            subject_text = " ".join([tok.text for tok in subject.subtree]).strip()
            object_text = " ".join([tok.text for tok in object.subtree])
            if(subject_text.lower() not in IGNORE_WORDS and object_text.lower() not in IGNORE_WORDS and len(subject_text.split()) <= 5 and len(object_text.split()) <= 5):     
                triples.append((subject_text, relation, object_text))

    return list(set(triples))

def custom_relations(text):
    triples = []
    doc = nlp(text)
    for sent in doc.sents:
        sentence = sent.text.lower()
        entities = [(ent.text, ent.label_) for ent in sent.ents]

        persons = [e[0] for e in entities if e[1] == "PERSON"]
        orgs = [e[0] for e in entities if e[1] == "ORG"]
        locations = [e[0] for e in entities if e[1] in ["GPE", "LOC"]]
        dates = [e[0] for e in entities if e[1] == "DATE"]
        money = [e[0] for e in entities if e[1] == "MONEY"]

        persons = [p for p in persons if len(p.split()) <= 5]
        orgs = [o for o in orgs if len(o.split()) <= 5]
        locations = [l for l in locations if len(l.split()) <= 5]

        company=None
        #Founded
        if "founded by" in sentence:
            if len(orgs) > 0:
                company = orgs[0]
                for person in persons:
                    triples.append((person, "FOUNDED", company))

        elif "founded in" in sentence:
            if len(orgs) > 0:
                company = orgs[0]
                for date in dates:
                    triples.append((company, "FOUNDED_IN", date))

        #CEO Of
        if "ceo of" in sentence or "chief executive officer" in sentence:
            for person in persons:
                for org in orgs:
                    triples.append((person, "CEO_OF", org))

        #CEO SINCE
        if "became the ceo" in sentence:
            if len(persons) > 0:
                for date in dates:
                    triples.append((persons[0], "CEO_SINCE", date))

        #WORKS_AT
        if "works at" in sentence:
            for person in persons:
                for org in orgs:
                    triples.append((person, "WORKS_AT", org))

        # CHAIRMAN OF
        if "chairman of" in sentence:
            for person in persons:
                for org in orgs:
                    triples.append((person, "CHAIRMAN_OF", org))

        #ACQUIRED
        if "acquired" in sentence:
            if len(orgs) >= 2:
                triples.append((orgs[0], "ACQUIRED", orgs[1]))
                for date in dates:
                    triples.append((orgs[0], "ACQUIRED_IN", date))

        # HEADQUARTERED IN
        if "headquartered in" in sentence or "located in" in sentence:
            if len(orgs) > 0:
                company = orgs[0]
                for location in locations:
                    triples.append((company, "HEADQUARTERED_IN", location))

        # MONEY
        if len(orgs) > 0 and len(money) > 0:
            for amount in money:
                triples.append((orgs[0], "REVENUE", amount))
    return list(set(triples))