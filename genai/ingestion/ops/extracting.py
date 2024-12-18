from settings import (
    AZURE_DOCUMENT_INTELLIGENCE_API_KEY, 
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
)

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult, ContentFormat

def init_di():
    endpoint = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    credential = AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_API_KEY)
    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)

    return document_intelligence_client

def convert_to_markdown(raw_docs):
    document_intelligence_client = init_di()  
    markdown_docs = []

    try:
        for doc in raw_docs:
            content_bytes = doc['content'].getvalue()

            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-layout", 
                AnalyzeDocumentRequest(bytes_source=content_bytes), 
                output_content_format=ContentFormat.MARKDOWN
                )

            di_result: AnalyzeResult = poller.result()
            markdown_docs.append(Document(
                metadata = {"file_path": doc['blob_name']},
                page_content = di_result.content
            ))
            return markdown_docs

    except Exception as e:
        print(f"Error occurred while analyzing the document: {e}")
        return None