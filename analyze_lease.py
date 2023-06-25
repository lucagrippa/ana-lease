import streamlit as st

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain


def get_questions():
    questions = [
        "Does it say there is fixtures and furniture that come with the apartment? If so, flag these for the tenant so they can look for them when they move in and make sure they work on the day they move in.",
        "Are there any references to “objectionable conduct” in the lease? If so, flag the section for the tenant and check if it is defined. Also note what the consequences are for objectionable conduct.",
        "What are the reasons that allow the landlord to terminate the lease?.",
        "Can the tenant ever terminate the lease? When can the tenant terminate the lease?",
        "Are there any instances where the landlord changes the tenant a fee for anything? Please list these instances and the sections of the lease.",
        "If there are any parts of the lease that make the tenant liable for negligence? If so, suggest asking the landlord to change this to say 'gross negligence'",
        "Is the tenant being asked to indemnify the landlord for anything? Please list these reasons and flag the sections of the lease.",
        "Is the tenant required to take out renter's insurance? If so, what section of the lease specifies this? How much is the insurance supposed to be for? Include a link to Lemonade.",
        "Is there a confidentiality requirement anywhere in the lease?",
        "Does the lease include a “lead paint disclosure”? If so, note the section where this is in the lease. Suggest asking the landlord to explain this.",
    ]

    return questions

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")
    return vectorstore


def ask_questions(llm):
    vectorstore = get_vectorstore()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

    with st.expander("Specific Questions:"):
        for num, question in enumerate(get_questions(), start=1):
            response = qa_chain.run(question)

            with st.container():
                st.write(f"{num}. {question}")
                st.write(f" - {response}")
                st.divider()



def summarize_document(llm, pages):
#     REFINE_PROMPT_TMPL = """
# You are a expert real estate attorney in NYC. Your mission is to help non-lawyers understand their lease agreement, warn them of any unsual clauses and give advice.
# Your job is to produce a concise summary of any negative terms of a rental agreement.
# We have provided an existing summary up to a certain point: {existing_answer}
# We have the opportunity to refine the existing summary (only if needed) with some more context below.
# ------------
# {text}
# ------------

# Given the new context, refine the original summary
# If the context isn't useful, return the original summary.
# """

#     REFINE_PROMPT = PromptTemplate(
#         input_variables=["existing_answer", "text"],
#         template=REFINE_PROMPT_TMPL,
#     )

    prompt_template = """
You are a expert real estate attorney in NYC. Your mission is to help non-lawyers understand their lease agreement, warn them of any unsual clauses and give advice.
Write concise bullet points of any negative terms for a potential tenant of the following rental agreement. If there are no negative terms of the agreement then you do not need to write any bullet points:

"{text}"


BULLET POINTS:
"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

    chain = load_summarize_chain(
        llm, 
        chain_type="map_reduce", 
        # question_prompt=PROMPT, 
        map_prompt=PROMPT,
        combine_prompt=PROMPT,
        # refine_prompt=REFINE_PROMPT,
        verbose=True
    )
    summary = chain.run(pages)

    with st.expander("Summary:"):
        st.write(summary)


def analyze_lease(pages):
    llm = ChatOpenAI(temperature=0.0)

    ask_questions(llm)

    summarize_document(llm, pages)

    # 1. Does it say there is fixtures and furniture that come with the apartment? If so, flag these for the tenant so they can look for them when they move in and make sure they work on the day they move in.
    # 2. Are there any references to “objectionable conduct” in the lease? If so, flag the section for the tenant and check if it is defined. Also note what the consequences are for objectionable conduct.
    # 3. What are the reasons that allow the landlord to terminate the lease? List these in 6 words each.
    # 4. Can the tenant ever terminate the lease? When can the tenant terminate the lease?
    # - Look for statutory reasons that allow tenants to terminate and contrast
    # 5. Are there any instances where the landlord changes the tenant a fee for anything? Please list these instances and the sections of the lease.
    # 6. If there are any parts of the lease that make the tenant liable for negligence? If so, suggest asking the landlord to change this to say “gross negligence”
    # 7. Is the tenant being asked to indemnify the landlord for anything? Please list these reasons and flag the sections of the leas.e
    # - Contrasts against statutory circumstances where tenants are permitted to indemnify landlords
    # 8.Is the tenant required to take out renter’s insurance? If so, what section of the lease specifies this? How much is the insurance supposed to be for? Include a link to Lemonade.
    # 9. Is there a confidentiality requirement anywhere in the lease?
    # 10. Does the lease include a “lead paint disclosure”? If so, note the section where this is in the lease. Suggest asking the landlord to explain this.