from document_reader import extract_text_document
from entityextractor import extract_entities

filepath = r"C:\Users\Lenovo\OneDrive\Desktop\Knowledge Graph ntcc\KnowledgeGraphBuilder\data\sampledocs\Nevaeh Singh NTCC 4144.pdf"

print("\nReading document...")
text = extract_text_document(filepath)

print("\nExtracting entities...")
entities = extract_entities(text)

print("\nEntities Found:\n")
for e in entities:
    print(e)