import streamlit as st
import tempfile
from src.document_reader import extract_text_document
from src.entityextractor import extract_entities

# App Title
st.title("Automated Knowledge Graph Builder")
st.write("Upload a document and extract entities automatically.")

# File Upload
uploaded_file = st.file_uploader(
    "Upload PDF or TXT file",
    type=["pdf", "txt"]
)

# Process Button
if uploaded_file is not None:
    if st.button("Process Document"):

        # Save uploaded file temporarily
        # Get original file extension
        file_extension = uploaded_file.name.split(".")[-1]

# Save uploaded file with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + file_extension) as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name


        # Step 1: Extract text
        st.subheader("Extracted Text Preview")
        text = extract_text_document(temp_path)

        if len(text.strip()) == 0:
            st.error("No text could be extracted from this file.")
        else:
            st.write(text[:500])  # show first 500 chars

            # Step 2: Extract entities
            st.subheader("Extracted Entities")
            entities = extract_entities(text)

            if len(entities) == 0:
                st.warning("No entities found.")
            else:
                for ent in entities:
                    st.write(ent)