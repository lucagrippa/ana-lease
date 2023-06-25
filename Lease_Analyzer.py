import os
import random
from dotenv import load_dotenv

import streamlit as st
from streamlit_chat import message

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from analyze_lease import analyze_lease

def embed_and_store(documents):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db_analyzer")
    vectorstore.persist()

    return vectorstore

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(embedding_function=embeddings, persist_directory="./chroma_db_analyzer")
    return vectorstore


def delete_file(file_path):
    # Check if the file exists before deleting
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print("File deleted successfully.")
    else:
        print("File does not exist.")


def get_uploaded_file_texts(uploaded_file):
    # Specify the desired file path to save the uploaded file
    save_directory = "./lease"

    # Get the filename of the uploaded file
    file_name = uploaded_file.name

    # Specify the file path to save the uploaded file
    save_path = os.path.join(save_directory, file_name)

    # Save the uploaded file to the specified path
    with open(save_path, "xb") as file:
        file.write(uploaded_file.read())

    loader = PyPDFLoader(save_path)
    pages = loader.load_and_split()

    delete_file(save_path)
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        separators=["\n\n", "\n"],
        chunk_size = 1500,
        chunk_overlap  = 300,
        length_function = len,
    )

    texts = text_splitter.split_documents(pages)

    return texts, pages


def main():
    load_dotenv()  # take environment variables from .env.

    st.title("📝 Lease Analyzer")

    if "analyzed" not in st.session_state:
        st.session_state["analyzed"] = False

    if "pages" not in st.session_state:
        st.session_state["pages"] = []

    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = ""

    if st.session_state["analyzed"] is False:
        uploaded_file = st.file_uploader("Upload your lease!", type="pdf")
        analyze_button = st.button("Analyze")
    else:
        status_container = st.container()
        # Load and embed document if file is uploaded
        with st.spinner("Analyzing your document..."):
            texts, pages = get_uploaded_file_texts(st.session_state["uploaded_file"])
            st.session_state["pages"] = pages
            _ = embed_and_store(texts)
            # analyze document function goes here
            analyze_lease(st.session_state["pages"])

            st.session_state["analyzed"] = True
            status_container.success("Your document has been successfully analyzed!", icon="✅")

    if analyze_button and uploaded_file is not None:
        st.session_state["uploaded_file"] = uploaded_file
        st.session_state["analyzed"] = True
        st.experimental_rerun()


if __name__ == "__main__":
    main()