import pandas as pd
import streamlit as st
import tempfile
from src.document_reader import extract_text_document
from src.entityextractor import extract_entities, remove_duplicates

# Initialize entities
entities = []

st.title("Automated Knowledge Graph Builder")
st.write("Upload a document for entity extraction")

st.sidebar.title("Project Info")
st.sidebar.write("Automated Knowledge Graph Builder using NLP")

# File Upload
uploaded_file = st.file_uploader(
    "Upload PDF, TXT file or DOCX file",
    type=["pdf", "txt", "docx"]
)

# Process Button
if uploaded_file is not None:
    if st.button("Process Document"):

        file_extension = uploaded_file.name.split(".")[-1]

        # Save uploaded file with correct extension
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix="." + file_extension
        ) as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        # Step 1: Extract text
        st.subheader("Extracted Text Preview")
        text = extract_text_document(temp_path)

        if len(text.strip()) == 0:
            st.error("No text could be extracted from this file.")
        else:
            st.text_area(
                "Document Text",
                text[:1000],
                height=300
            )
            st.success("File uploaded successfully!")

            # Step 2: Extract entities

            entities = extract_entities(text)
            entities = remove_duplicates(entities)

            if len(entities) == 0:
                st.warning("No entities found.")
            else:
                df = pd.DataFrame(
                    entities,
                    columns=["Entity", "Type"]
                )

                


                # Interactive dataframe
                st.subheader("Extracted Entities")
                st.dataframe(
                    df,
                    use_container_width=True
                )
                # Metrics
                
                st.metric("Entities Found", len(entities))