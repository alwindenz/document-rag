from .ops.loading import load_to_blob, convert_to_bytes
from .ops.extracting import convert_to_markdown
from .ops.parsing import extract_elements
from .ops.chunking import split_text_elements, split_table_elements
from .ops.vectorstore import add_to_ai_search
from .utils.logging import logger

def ingestion(file):
    raw_docs = get_raw_docs(load_to_blob(file))
    markdown_docs = convert_to_markdown(raw_docs)

    text_chunks = split_text_elements(*extract_elements(markdown_docs))
    table_chunks = split_table_elements(*extract_elements(markdown_docs, is_table=True))

    vectorstore = add_to_ai_search(text_chunks + table_chunks)

    return vectorstore

if __name__ == "__main__":
    logger.info("Ingestion started.")
    vectorstore = ingestion()
    logger.info("Ingestion complete. Vectorstore is ready for use.")