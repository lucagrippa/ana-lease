import streamlit as st

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain

from vectorstore import get_vectorstore
from questions import get_lease_summary_questions, get_counsel_questions

def lease_summary(llm):
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    {question}"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT, "verbose": True}
    vectorstore = get_vectorstore()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=vectorstore.as_retriever(search_kwargs={"namespace": "lease-demo"}), 
        chain_type_kwargs=chain_type_kwargs,
    )

    # st.title("Important Questions:")
    questions, titles = get_lease_summary_questions()

    # st.write("## Summary")
    responses = []
    for question, title in zip(questions, titles):
        response = qa_chain.run(question)
        responses.append({
            "title": title,
            "response": response
        })

        # with st.container():
        #     st.write(f"{title}: {response}")

    st.session_state["summary"] = responses


def lease_consel_analysis(llm):
    prompt_template = """You are an expert real estate attorney. Use the following pieces of context to answer the question at the end in 2-3 bullet points.
    Offer advice on how you would change the contract in the tenants favor.
    The answer should be easy to understand even by primary school students.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    {question}"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT, "verbose": True}
    vectorstore = get_vectorstore()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=vectorstore.as_retriever(search_kwargs={"namespace": "lease-demo"}), 
        chain_type_kwargs=chain_type_kwargs,
    )

    # st.title("Important Questions:")
    questions, titles = get_counsel_questions()

    # st.write("## Summary")
    responses = []
    for question, title in zip(questions, titles):
        response = qa_chain.run(question)
        responses.append({
            "title": title,
            "response": response
        })

    st.session_state["counsel"] = responses


def analyze_lease(pages):
    llm = ChatOpenAI(temperature=0.0)

    print("Asking summary questions")
    lease_summary(llm)

    print("Asking counsel questions")
    lease_consel_analysis(llm)







