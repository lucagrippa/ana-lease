import streamlit as st


def main():
    st.title("📝 Lease Analyzer")
    uploaded_lease = st.file_uploader("Upload your lease!", type="pdf")


if __name__ == "__main__":
    main()