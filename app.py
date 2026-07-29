import pandas as pd #python -m streamlit run app.py
import streamlit as st
import tempfile
import plotly.express as px
import time 
from src.document_reader import extract_text_document
from src.relation_extractor import extract_relations, custom_relations
from src.entityextractor import extract_entities, remove_duplicates
from src.preprocessing import preprocess
from connect import store_triples, test_connection, graph_stats, generate_graph, clear_graph

st.title("Automated Knowledge Graph Builder")
st.write("Transform research papers, articles, PDFs and documents into interactive knowledge graphs using NLP and Neo4j.")

st.sidebar.title("Project Information")
st.sidebar.write("Automated Knowledge Graph Builder using NLP and Neo4j")

try:
    st.sidebar.header("Neo4j is: ")
    st.sidebar.success(test_connection())
except:
    st.sidebar.error("🔴 Disconnected")

# File Upload
uploaded_file = st.file_uploader(
    "Upload PDF, TXT or DOCX File",
    type=["pdf", "txt", "docx"]
)

# Process Document
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

        with st.spinner("Processing document..."):
            text = extract_text_document(temp_path)
            if len(text.strip()) == 0:
                st.error("No text could be extracted.")
                st.stop()

            processed_text = preprocess(text)

            entities = extract_entities(text)
            entities = remove_duplicates(entities)

            general_relations = extract_relations(text)
            custom_relations_list = custom_relations(text)

            triples = list(set(general_relations + custom_relations_list))

            st.session_state["text"] = text
            st.session_state["processed_text"] = processed_text
            st.session_state["entities"] = entities
            st.session_state["triples"] = triples
            st.session_state["graph_created"] = False

# Display Results
if "entities" in st.session_state:
    text = st.session_state["text"]
    processed_text = st.session_state["processed_text"]
    entities = st.session_state["entities"]
    triples = st.session_state["triples"]

    # Statistics Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Entities", len(entities))
    col2.metric("Relations", len(triples))
    col3.metric("Words", len(text.split()))
    col4.metric("Characters", len(text))

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Text",
            "Entities",
            "Relations",
            "Knowledge Graph"
        ]
    )

    # TEXT TAB
    with tab1:
        st.subheader("Extracted Text Preview")
        st.text_area(
            "Original Text",
            text[:1000],
            height=250
        )

        with st.expander("Processed Text"):
            st.text_area(
                "Processed Text",
                processed_text[:1000],
                height=200
            )

    # ENTITIES TAB
    with tab2:
        if len(entities) == 0:
            st.warning("No entities found.")
        else:
            df = pd.DataFrame(
                entities,
                columns=["Entity", "Type"]
            )
            df.insert(
                0,
                "S.No",
                range(1, len(df) + 1)
            )
            st.subheader("Extracted Entities")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            entity_types = df["Type"].value_counts()
            color_map={
                "PERSON": "#EF4444", 
                "ORG": "#F5D20B", 
                "GPE": "#10B981",
                "DATE": "#3B82F6", 
                "MONEY": "#8B5CF6" 
            }
            fig= px.bar( 
                        x=entity_types.index,
                        y=entity_types.values,
                        color=entity_types.index,
                        color_discrete_map=color_map,
                        labels={"x": "Entity Type", "y": "Number of Entities"},
                        title="Entity Distribution")
            st.plotly_chart(fig, use_container_width=True)
            st.download_button(
                "Download Entities CSV",
                df.to_csv(index=False),
                file_name="entities.csv",
                mime="text/csv"
            )

    # RELATIONS TAB
    with tab3:
        st.subheader("Extracted Relationships")
        if len(triples) == 0:
            st.warning("No relationships found.")
        else:
            relation_df = pd.DataFrame(
                triples,
                columns=[
                    "Subject",
                    "Relation",
                    "Object"
                ]
            )
            st.dataframe(
                relation_df,
                use_container_width=True
            )
            st.metric(
                "Total Triples",
                len(triples)
            )

# KNOWLEDGE GRAPH TAB
    with tab4:
        st.subheader("Knowledge Graph")
        col1, col2 = st.columns(2)
        with col1:
            build_graph = st.button("Build Knowledge Graph", type="primary")
        with col2:
            clear_db = st.button("Clear Knowledge Graph")

        # Clear Graph
        if clear_db:
            try:
                clear_graph()
                st.session_state["graph_created"] = False
                st.success("Knowledge Graph Cleared Successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        # Build Graph
        if build_graph:
            try:
                start_time= time.time() #Start timer
                with st.spinner("Creating Knowledge Graph..."):
                    store_triples(triples)
                    st.session_state["graph_created"] = True
                end_time= time.time() #end timer
                st.session_state["graph_time"]= end_time- start_time
            except Exception as e:
                st.error(f"Error: {e}")

        # Display graph if already built
        if st.session_state.get("graph_created", False):
            try:
                nodes, relations = graph_stats()
                st.success(f"Knowledge Graph Created Successfully! "f"({len(triples)} triples stored)")
                col1, col2 = st.columns(2)
                graph_file = generate_graph()
                with open(graph_file, "r", encoding="utf-8") as file:
                    html = file.read()
                st.subheader("Knowledge Graph Visualization")
                st.components.v1.html(html, height=750, scrolling=True)
                st.info(f"Graph Generation Time: {st.session_state['graph_time']:.2f} seconds")
            except Exception as e:
                st.error(f"Error: {e}")