from src.relation_extractor import extract_relations, custom_relations
from connect import store_triples

text = """
Elon Musk founded SpaceX in 2002. SpaceX is headquartered in California, USA. Elon Musk is also the CEO of Tesla. Tesla develops electric vehicles and renewable energy solutions. 
Sundar Pichai works at Google as the Chief Executive Officer. Google was founded by Larry Page and Sergey Brin in California. Google focuses on artificial intelligence and cloud computing technologies.
Satya Nadella became the CEO of Microsoft in 2014. Microsoft is located in Redmond, Washington. Microsoft develops software products and cloud services.
Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976. Apple is famous for products like the iPhone and MacBook. Apple generated $416.16 billion revenue.
Ratan Tata was the chairman of Tata Group. Tata Group is headquartered in Mumbai, India. Tata Motors developed innovative automobiles and expanded globally. Tata Group acquired Jaguar Land Rover in 2008.
Marie Curie discovered Radium and Polonium.
India signed a document with France.
"""

# Extract relations
general_triples = extract_relations(text)
custom_triples = custom_relations(text)

# Combine and remove duplicates
triples = list(set(general_triples + custom_triples))

print("\nEXTRACTED TRIPLES\n")
for triple in triples:
    print(triple)

print(f"\nTotal Triples: {len(triples)}")
# Store in Neo4j
store_triples(triples)
print("\nKnowledge Graph Stored Successfully!")