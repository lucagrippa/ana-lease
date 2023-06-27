import os
import random
from dotenv import load_dotenv

import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from vectorstore import get_uploaded_file_texts, get_vectorstore, embed_and_store
from scripts.delete_vectors import delete_vectors


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
        vectorstore.as_retriever(search_kwargs={"namespace": "lease-demo"}), 
        memory=memory, 
        combine_docs_chain_kwargs=combine_docs_chain_kwargs,
        verbose=True
    )

    return chain


def main():
    load_dotenv()  # take environment variables from .env.

    st.title("📝 LeasePilot ChatBot")

    if "memory" not in st.session_state:
        st.session_state["memory"] = None

    if "lease_uploaded" not in st.session_state:
        st.session_state["lease_uploaded"] = False

    if "analyzed" not in st.session_state:
        st.session_state["analyzed"] = False

    if "chunks" not in st.session_state:
        st.session_state["chunks"] = []

    if "pages" not in st.session_state:
        st.session_state["pages"] = []


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
    else:
        new_document_button = st.button("Upload a new lease")
        with st.form("chat_input", clear_on_submit=True):
            a, b = st.columns([4, 1])
            user_input = a.text_input(
                label="Your message:",
                placeholder="What questions do you have about your lease?",
                label_visibility="collapsed",
            )
            b.form_submit_button("Send", use_container_width=True)

        if new_document_button:
            delete_vectors()
            st.session_state["lease_uploaded"] = False
            st.experimental_rerun()

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