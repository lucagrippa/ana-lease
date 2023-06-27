import os
import random
from dotenv import load_dotenv

import streamlit as st
from streamlit_chat import message

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain

from analyze_lease import analyze_lease
from vectorstore import get_uploaded_file_texts, embed_and_store
from scripts.delete_vectors import delete_vectors


def main():
    load_dotenv()  # take environment variables from .env.

    st.title("📝 Lease Analyzer")

    if "lease_uploaded" not in st.session_state:
        st.session_state["lease_uploaded"] = False

    if "analyzed" not in st.session_state:
        st.session_state["analyzed"] = False
    
    if "chunks" not in st.session_state:
        st.session_state["chunks"] = []

    if "pages" not in st.session_state:
        st.session_state["pages"] = []

    if "summary" not in st.session_state:
        st.session_state["summary"] = []

    if "counsel" not in st.session_state:
        st.session_state["counsel"] = []

    if "health_score" not in st.session_state:
        st.session_state["health_score"] = random.randint(75,100)

    if st.session_state["lease_uploaded"] is False:
        with st.form("my_form"):
            uploaded_file = st.file_uploader("Upload your lease!", type="pdf")
            # Every form must have a submit button.
            uploaded = st.form_submit_button("Upload lease")

        if uploaded and uploaded_file is not None:
            with st.spinner("Uploading your lease..."):
                chunks, pages = get_uploaded_file_texts(uploaded_file)
                embed_and_store(chunks)
                st.session_state["chunks"] = chunks
                st.session_state["pages"] = pages
                memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
                st.session_state["memory"] = memory

            st.session_state["lease_uploaded"] = True
            st.experimental_rerun()
    elif st.session_state["analyzed"] is False:
        status_container = st.container()
        # Load and embed document if file is uploaded
        with st.spinner("Analyzing your lease..."):
            # analyze document function goes here
            analyze_lease(st.session_state["pages"])

            st.session_state["analyzed"] = True
            st.experimental_rerun()

    elif st.session_state["analyzed"] is True:
        new_document_button = st.button("Upload a new lease")

        if new_document_button:
            delete_vectors()
            st.session_state["lease_uploaded"] = False
            st.session_state["analyzed"] = False
            st.experimental_rerun()

        st.success("Your document has been successfully analyzed!", icon="✅")
        
        # Health Score
        with st.container():
            st.write(f"### Contract Health Score = {st.session_state['health_score']}/100")

        # Summary
        st.write("### Summary")
        with st.expander("Click to expand"):
            for response in st.session_state["summary"]:
                st.write(f"{response['title']}: {response['response']}")

        # Counsel Analysis
        st.write("### Counsel Analysis")
        with st.expander("Click to expand"):
            for response in st.session_state["counsel"]:
                st.write(f"{response['title']}: {response['response']}")



if __name__ == "__main__":
    main()