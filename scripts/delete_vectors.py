import os
import pinecone
from dotenv import load_dotenv


def delete_vectors():
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV")  # next to api key in console
    )

    index_name = "lease-analyzer"
    index = pinecone.Index(index_name)
    index.delete(deleteAll="true", namespace="lease-demo")


def main():
    load_dotenv()  # take environment variables from .env.
    delete_vectors()

if __name__ == "__main__":
    main()