from settings import (
    AZURE_AI_SEARCH_SERVICE_NAME, 
    AZURE_AI_SEARCH_INDEX_NAME, 
    AZURE_AI_SEARCH_API_KEY, 
)

from langchain_community.retrievers import AzureAISearchRetriever
from azure.core.credentials import AzureKeyCredential
import json

def retriever_from_ai_search(question):
    retriever = AzureAISearchRetriever(
    content_key="content", top_k=3, 
    index_name=AZURE_AI_SEARCH_INDEX_NAME,
    service_name=AZURE_AI_SEARCH_SERVICE_NAME,
    api_key=AZURE_AI_SEARCH_API_KEY,
    )
    results = retriever.invoke(question)

    return results