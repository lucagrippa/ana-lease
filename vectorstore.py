import os
import pinecone

from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


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
        chunk_size = 1250,
        chunk_overlap  = 250,
        length_function = len,
    )

    texts = text_splitter.split_documents(pages)

    return texts, pages


def embed_and_store(documents):
    vectorstore = get_vectorstore()
    vectorstore.add_texts(
        [document.page_content for document in documents],
        [document.metadata for document in documents],
        namespace="lease-demo"
    )


def get_vectorstore():
    # initialize pinecone
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV")  # next to api key in console
    )

    index_name = "lease-analyzer"
    embeddings = OpenAIEmbeddings()
    vectorstore = Pinecone.from_existing_index(index_name, embeddings)

    return vectorstore