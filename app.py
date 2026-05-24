import pandas as pd
import streamlit as st
import tempfile
from src.document_reader import extract_text_document
from src.entityextractor import extract_entities

st.title("Automated Knowledge Graph Builder")
st.write("Upload a document from entity extraction")

# File Upload
uploaded_file = st.file_uploader(
    "Upload PDF, TXT file or DOCX file",
    type=["pdf", "txt", "docx"]
)

# Process Button
if uploaded_file is not None:        #Run next code only after user uploads a file.
    if st.button("Process Document"): 
        file_extension = uploaded_file.name.split(".")[-1]

# Save uploaded file with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + file_extension) as tmp_file:   #Creates temporary file
            tmp_file.write(uploaded_file.read())     #Uploaded file data in temp file
            temp_path = tmp_file.name


        # Step 1: Extract text
        st.subheader("Extracted Text Preview")
        text = extract_text_document(temp_path) 

        if len(text.strip()) == 0:
            st.error("No text could be extracted from this file.")
        else:
            st.text_area("Document Text", text[:1000], height=300)
            st.success("File uploaded successfully!")

            # Step 2: Extract entities
            st.subheader("Extracted Entities")
            entities = extract_entities(text)

            if len(entities) == 0:
                st.warning("No entities found.")
            else:
                df = pd.DataFrame(entities, columns=["Entity", "Type"])    #In a tabluar format
                st.table(df)