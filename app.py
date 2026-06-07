import pandas as pd
import streamlit as st
import tempfile
from src.document_reader import extract_text_document
from src.relation_extractor import extract_relations, custom_relations
from src.entityextractor import extract_entities, remove_duplicates
from src.preprocessing import preprocess

# Initialize entities

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

        #with st.spinner("Processing document...")

        # Step 1: Extract text
        st.subheader("Extracted Text Preview")
        text = extract_text_document(temp_path)

        if len(text.strip()) == 0:
            st.error("No text could be extracted from this file.")
        else:
            st.text_area("Document Text", text[:1000], height=300)
            st.success("Document processed successfully!")

            processed_text = preprocess(text)
            st.subheader("Processed Text")
            st.text_area("Cleaned Text", processed_text[:1000], height=250)

            # Step 2: Extract entities
            entities = extract_entities(text)
            entities = remove_duplicates(entities)
            triples = extract_relations(text)
            triples = custom_relations(text)

            if len(entities) == 0:
                st.warning("No entities found.")
            else:
                # Create DataFrame
                df = pd.DataFrame(entities, columns=["Entity", "Type"])

                # Add serial number column starting from 1
                df.insert(0, "S.No", [str(i) for i in range(1, len(df) + 1)])

                # Display table
                st.subheader("Extracted Entities")
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Metrics
                st.metric("Entities Found",len(entities))
                st.metric("Characters", len(text))
                st.metric("Words", len(text.split()))

                entity_types = df["Type"].value_counts()
                st.subheader("Entity Type Distribution")
                st.bar_chart(entity_types)

                st.subheader("Extracted Relationships")
                if len(triples) == 0:
                    st.warning("No relationships found.")
                else:
                    relation_df = pd.DataFrame(triples,columns=["Subject", "Relation", "Object"])
                    st.dataframe(relation_df,use_container_width=True)
                    st.metric("Relationships Found",len(triples))
                    st.metric("Unique Relations",relation_df["Relation"].nunique())