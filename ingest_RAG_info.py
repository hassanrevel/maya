from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone as PineconeClient
from llms import embeddings
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
pc = PineconeClient()
index = pc.Index("wellington-grace-hospital-info")

vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Load and split
loader = TextLoader("data/hospital_info.txt", encoding="utf-8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

vector_store.add_documents(documents=chunks)