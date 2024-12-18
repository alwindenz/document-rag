from .ops.loading import load_to_blob, convert_to_bytes
from .ops.extracting import convert_to_markdown
from .ops.parsing import extract_elements
from .ops.chunking import split_text_elements, split_table_elements
from .ops.vectorstore import add_to_ai_search
from .utils.logging import logger

def ingestion(file):
    file_name = load_to_blob(file)
    raw_docs = convert_to_bytes(file_name)
    logger.info(f"These are the raw docs: {raw_docs}")
    markdown_docs = convert_to_markdown(raw_docs)
    logger.info(f"These are the markdown docs: {markdown_docs}")

    text_elements, table_elements = extract_elements(markdown_docs)
    text_chunks = split_text_elements(text_elements)
    table_chunks = split_table_elements(table_elements)
    logger.info(f"Text chunks: {text_chunks}")
    logger.info(f"Table chunks: {table_chunks}")

    all_chunks = text_chunks + table_chunks
    vectorstore = add_to_ai_search(all_chunks)

    return vectorstore


if __name__ == "__main__":
    logger.info("Ingestion started.")
    vectorstore = ingestion()
    logger.info("Ingestion complete. Vectorstore is ready for use.")