import os
import tempfile
import streamlit as st
from streamlit_chat import message

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

def get_vectorstore(documents):
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings)

    return vectorstore

def get_conversational_qa_chain(vectorstore, memory):
    llm = OpenAI(temperature=0.0)
    chain = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)

    return chain


def delete_file(file_path):
    # Check if the file exists before deleting
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print("File deleted successfully.")
    else:
        print("File does not exist.")


def main():
    st.title("📝 Lease Analyzer")
    uploaded_file = st.file_uploader("Upload your lease!", type="pdf")

    analyze_button = st.button("Analyze")

    if "memory" not in st.session_state:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        st.session_state["memory"] = memory

    if "file_embedded" not in st.session_state:
        st.session_state["file_embedded"] = False

    with st.form("chat_input", clear_on_submit=True):
        a, b = st.columns([4, 1])
        user_input = a.text_input(
            label="Your message:",
            placeholder="What questions do you have about your lease?",
            label_visibility="collapsed",
        )
        b.form_submit_button("Send", use_container_width=True)


    for msg in st.session_state["memory"].load_memory_variables({})["chat_history"]:
        if msg.type == "ai":
            message(msg.content, is_user=False)
        else:
            message(msg.content, is_user=True)

        
    if user_input and uploaded_file is not None:
        message(user_input, is_user=True)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        message(msg.content)


    # Load document if file is uploaded
    if uploaded_file is not None and analyze_button and st.session_state["file_embedded"] is False:
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
            chunk_size = 100,
            chunk_overlap  = 20,
            length_function = len,
        )

        texts = text_splitter.split_documents(pages)

        vectorstore = get_vectorstore(texts)

        


        st.write(texts[0])



if __name__ == "__main__":
    main()