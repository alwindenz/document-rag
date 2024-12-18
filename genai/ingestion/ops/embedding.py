from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

def embedding_function():
    embedding_model = OpenAIEmbeddings(model = 'text-embedding-ada-002')
    return embedding_model