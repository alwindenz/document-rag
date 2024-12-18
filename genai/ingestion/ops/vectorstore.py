from settings import (
    AZURE_AI_SEARCH_SERVICE_NAME, 
    AZURE_AI_SEARCH_INDEX_NAME, 
    AZURE_AI_SEARCH_API_KEY, 
    AZURE_AI_SEARCH_ENDPOINT
)

from typing import List
from langchain.docstore.document import Document
from ..utils.logging import logger

from azure.core.credentials import AzureKeyCredential
from langchain_community.vectorstores.azuresearch import AzureSearch
from azure.search.documents import SearchClient
from .embedding import embedding_function

def add_to_ai_search(chunks: List[Document]):
    search_client = SearchClient(
        endpoint=AZURE_AI_SEARCH_ENDPOINT,
        index_name=AZURE_AI_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_AI_SEARCH_API_KEY)
    )
    
    existing_ids = set()
    results = search_client.search(search_text="*", select="id", include_total_count=True)
    for result in results:
        existing_ids.add(result["id"])
    
    new_chunks = [chunk for chunk in chunks if chunk.id not in existing_ids]
    
    if new_chunks:
        vectorstore = AzureSearch(
            azure_search_endpoint=AZURE_AI_SEARCH_ENDPOINT,
            azure_search_key=AZURE_AI_SEARCH_API_KEY,
            index_name=AZURE_AI_SEARCH_INDEX_NAME
            embedding_function=embedding_function()
        )
        vectorstore.add_documents(documents=new_chunks)

    return vectorstore
