from document_reader import extract_text_document
filepath=r"C:\Users\Lenovo\OneDrive\Desktop\Knowledge Graph ntcc\KnowledgeGraphBuilder\data\sampledocs\Sample document KG.pdf"
text= extract_text_document(filepath)

print("\nExtracted Text: \n")
print(text[:500]) #print first 500 characters