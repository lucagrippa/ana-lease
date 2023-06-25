import tempfile
import streamlit as st
from langchain.document_loaders import PyPDFLoader


def main():
    st.title("📝 Lease Analyzer")
    uploaded_lease = st.file_uploader("Upload your lease!", type="pdf")

    analyze_button = st.button("Analyze")

    loader = PyPDFLoader("example_data/layout-parser-paper.pdf")
    pages = loader.load_and_split()


if __name__ == "__main__":
    main()