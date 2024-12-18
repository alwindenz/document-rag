from typing import Tuple, List, Dict
from langchain.docstore.document import Document
import re

def extract_elements(markdown_docs: List[Document]) -> Tuple[List[Document], List[Document]]:
    text_elements = []
    table_elements = []
    CONTEXT_LENGTH = 100  

    for doc in markdown_docs:
        content = doc.page_content  
        metadata = doc.metadata

        tables = re.findall(r"<table>.*?</table>", content, flags=re.DOTALL)
        for table in tables:
            table_start_idx = content.find(table)
            context_start_idx = max(0, table_start_idx - CONTEXT_LENGTH)
            context = content[context_start_idx:table_start_idx].strip()

            table_metadata = metadata.copy()
            table_metadata["type"] = "table"
            table_metadata["context"] = context
            table_elements.append(Document(metadata=table_metadata, page_content=table))

        text_content = re.sub(r"<table>.*?</table>", "", content, flags=re.DOTALL).strip()
        if text_content:
            text_metadata = metadata.copy()
            text_metadata["type"] = "text"
            text_elements.append(Document(metadata=text_metadata, page_content=text_content))

    return text_elements, table_elements
    