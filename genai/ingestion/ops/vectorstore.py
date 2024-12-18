from settings import (
    AZURE_COGNITIVE_SEARCH_SERVICE_NAME, 
    AZURE_COGNITIVE_SEARCH_INDEX_NAME, 
    AZURE_COGNITIVE_SEARCH_API_KEY, 
    AZURE_COGNITIVE_SEARCH_ENDPOINT
)

from typing import List
from langchain.docstore.document import Document

from azure.core.credentials import AzureKeyCredential
from langchain_community.vectorstores.azuresearch import AzureSearch
from azure.search.documents import SearchClient

def add_to_ai_search(chunks: List):
    search_client = SearchClient(
        endpoint=AZURE_COGNITIVE_SEARCH_ENDPOINT,
        index_name=AZURE_COGNITIVE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_COGNITIVE_SEARCH_API_KEY)
    )

    existing_ids = {result["id"] for result in search_client.search(search_text="*", select="id")}
    new_chunks = [chunk for chunk in chunks if chunk.id not in existing_ids]
    
    if new_chunks:
        vectorstore = AzureSearch(
            azure_search_endpoint=AZURE_COGNITIVE_SEARCH_ENDPOINT,
            azure_search_key=AZURE_COGNITIVE_SEARCH_API_KEY,
            index_name=AZURE_COGNITIVE_SEARCH_INDEX_NAME,
            embedding_function=embedding_function()
        )
        
        vectorstore.add_documents(documents=new_chunks)
        return vectorstore

    return None
