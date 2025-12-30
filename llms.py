# from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
# llm = ChatGroq(model='qwen-qwq-32b')
# llm = ChatGroq(model='llama-3.3-70b-versatile')
# llm = ChatOpenAI(
#     model='meta-llama/llama-4-scout:free',
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv('OPENROUTER_API_KEY')
# )

embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
