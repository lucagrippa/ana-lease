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
    vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db_bot")
    vectorstore.persist()

    return vectorstore

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(embedding_function=embeddings, persist_directory="./chroma_db_bot")
    return vectorstore


def get_conversational_qa_chain(vectorstore, memory):
    llm = ChatOpenAI(temperature=0.0)
    prompt_template = """
You are a expert real estate attorney in NYC. Your mission is to help non-lawyers understand their lease agreement, warn them of any unsual clauses and give advice.
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    combine_docs_chain_kwargs = {"prompt": PROMPT}

    chain = ConversationalRetrievalChain.from_llm(
        llm, 
        vectorstore.as_retriever(), 
        memory=memory, 
        combine_docs_chain_kwargs=combine_docs_chain_kwargs,
        verbose=True
    )

    return chain


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

    st.title("📝 Lease Bot")

    if "memory" not in st.session_state:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        st.session_state["memory"] = memory

    if "file_embedded" not in st.session_state:
        st.session_state["file_embedded"] = False


    if st.session_state["file_embedded"] is False:
        uploaded_file = st.file_uploader("Upload your lease!", type="pdf")

        chat_button = st.button("Chat with document")

        if chat_button and uploaded_file is not None:
            # Load and embed document if file is uploaded
            with st.spinner("Analyzing your document..."):
                texts, pages = get_uploaded_file_texts(uploaded_file)
                st.session_state["pages"] = pages
                _ = embed_and_store(texts)

                st.session_state["file_embedded"] = True
                st.experimental_rerun()

    else:
        with st.form("chat_input", clear_on_submit=True):
            a, b = st.columns([4, 1])
            user_input = a.text_input(
                label="Your message:",
                placeholder="What questions do you have about your lease?",
                label_visibility="collapsed",
            )
            b.form_submit_button("Send", use_container_width=True)


        # response container
        with st.container():
            output_container = st.empty()
            input_container = st.empty()

            # write chat message history
            for msg in list(reversed(st.session_state["memory"].load_memory_variables({})["chat_history"])):
                if msg.type == "ai":
                    message(msg.content, is_user=False, key=random.randint(0, 10000))
                else:
                    message(msg.content, is_user=True, key=random.randint(0, 10000))


            if user_input:
                vectorstore = get_vectorstore()
                memory = st.session_state["memory"]
                chain = get_conversational_qa_chain(vectorstore, memory)

                with input_container:
                    message(user_input, is_user=True, key=random.randint(0, 10000))

                with output_container:
                    with st.spinner("Analyzing your document..."):
                        response = chain({"question": user_input})
                    message(response["answer"], is_user=False, key=random.randint(0, 10000))
        

if __name__ == "__main__":
    main()