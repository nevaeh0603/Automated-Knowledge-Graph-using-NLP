from document_reader import extract_text_document
filepath=r"C:\Users\Lenovo\OneDrive\Desktop\Knowledge Graph ntcc\KnowledgeGraphBuilder\data\sampledocs\Nevaeh Singh NTCC 4144.pdf"
text= extract_text_document(filepath)

print("\nExtracted Text: \n")
print(text[:500]) #print first 500 characters