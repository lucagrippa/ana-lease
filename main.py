import os
import tempfile
import streamlit as st

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


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

    # Load document if file is uploaded
    if uploaded_file is not None and analyze_button:
         # Specify the desired file path to save the uploaded file
        save_directory = "/lease"

        # Get the filename of the uploaded file
        file_name = uploaded_file.name

        # Specify the file path to save the uploaded file
        save_path = os.path.join(save_directory, file_name)

        # Save the uploaded file to the specified path
        with open(save_path, "wb") as file:
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


        st.write(texts[0])



if __name__ == "__main__":
    main()