import os
import pinecone
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV")  # next to api key in console
)

index_name = "lease-analyzer"

pinecone.create_index(
    name=index_name, 
    dimension=1536,
)