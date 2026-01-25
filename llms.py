from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
# llm = ChatGroq(model='qwen-qwq-32b')
# llm = ChatGroq(model='llama-3.3-70b-versatile')
# llm = ChatGroq(model='openai/gpt-oss-20b')


embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
