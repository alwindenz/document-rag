import uuid
from typing import List
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_chunk_uuid(text: str) -> str:
    namespace = uuid.NAMESPACE_DNS
    chunk_uuid = str(uuid.uuid5(namespace, text))
    return chunk_uuid

def split_text_elements(text_elements: List[Document]) -> List[Document]:
    #logger.info('Chunking text elements...')

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
        ("#####", "Header 5"),
        ("######", "Header 6"),
    ]
    
    initial_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, 
        strip_headers=False)
    initial_text_chunks = []

    for doc in text_elements:
        content = doc.page_content
        metadata = doc.metadata.copy()

    initial_splits = initial_splitter.split_text(content)
    
    #logger.info('---- Header chunking...')
    for chunk in initial_splits:
        chunk_metadata = metadata.copy()
        chunk_uuid = get_chunk_uuid(str(chunk.metadata))
        chunk_metadata.update(chunk.metadata)
        chunk_metadata.update({
                        'chunk_uuid': chunk_uuid,
                    })

        initial_text_chunks.append(Document(
            page_content=chunk.page_content, 
            metadata=chunk_metadata))

    CHUNK_SIZE = 2000
    CHUNK_OVERLAP = 200
    
    final_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE, 
        chunk_overlap = CHUNK_OVERLAP)
    final_text_chunks = []

    #logger.info('---- Further recursive chunking...')
    for chunk in initial_text_chunks:
        chunk_index = 0
        if len(chunk.page_content) > CHUNK_SIZE:
            split_chunks = final_splitter.split_text(chunk.page_content)
            for split_chunk in split_chunks:
                new_metadata = chunk.metadata.copy()
                chunk_uuid = new_metadata['chunk_uuid']
                new_metadata.update({
                        'chunk_index': chunk_index,
                        'id': f'{chunk_uuid}-{chunk_index}'
                    })
                final_text_chunks.append(Document(page_content=split_chunk, metadata=new_metadata))
                chunk_index += 1
                
        else:
            new_metadata = chunk.metadata.copy()
            chunk_uuid = new_metadata['chunk_uuid']
            new_metadata.update({
                        'chunk_index': 0,
                        'id': f'{chunk_uuid}-{chunk_index}'
                    })
            final_text_chunks.append(Document(
                page_content=chunk.page_content, 
                metadata=new_metadata))

    #logger.info(f'Resulted in {len(final_text_chunks)} chunks for text elements')

    return final_text_chunks

def split_table_elements(table_elements: List[Document]) -> List[Document]:
    initial_table_chunks = []
    CHUNK_SIZE = 2000
    
    #logger.info('Chunking table elements...')
    for chunk in table_elements:
        if chunk.metadata.get('type') == 'table':
            soup = BeautifulSoup(chunk.page_content, 'html.parser')
            table = soup.find('table')
            rows = table.find_all('tr')
            chunk_uuid = get_chunk_uuid(chunk.page_content)

            header = str(rows[0])
            current_chunk = header
            current_length = len(header)

            chunk_index = 0

            for row in rows[1:]:
                row_str = str(row)
                row_length = len(row_str)

                if current_length + row_length > CHUNK_SIZE:
                    new_metadata = chunk.metadata.copy()
                    new_metadata.update({
                        'chunk_uuid': chunk_uuid,
                        'chunk_index': chunk_index,
                        'id': f'{chunk_uuid}-{chunk_index}'
                })
                    initial_table_chunks.append(Document(
                        page_content=f'<table>{current_chunk}</table>', 
                        metadata=new_metadata))

                    current_chunk = header + row_str
                    current_length = len(header) + row_length
                    chunk_index += 1
                else:
                    current_chunk += row_str
                    current_length += row_length

            if current_chunk:
                new_metadata = chunk.metadata.copy()
                new_metadata.update({
                        'chunk_uuid': chunk_uuid,
                        'chunk_index': chunk_index,
                        'id': f'{chunk_uuid}-{chunk_index}'
                })
                initial_table_chunks.append(Document(
                    page_content=f'<table>{current_chunk}</table>', 
                    metadata=new_metadata))
        else:
            initial_table_chunks.append(chunk)

    unique_ids = set()
    final_table_chunks = []

    for chunk in initial_table_chunks:
        chunk_id = chunk.metadata['id']
        if chunk_id not in unique_ids:
            unique_ids.add(chunk_id)
            final_table_chunks.append(chunk)

    #logger.info(f'Resulted in {len(final_table_chunks)} chunks for text elements')

    return final_table_chunks