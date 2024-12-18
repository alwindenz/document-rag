from azure.storage.blob import BlobServiceClient
import io

from settings import (
    AZURE_STORAGE_CONTAINER_NAME, 
    AZURE_STORAGE_ACCOUNT_NAME, 
    AZURE_STORAGE_ACCOUNT_KEY
)

def init_blob():
    AZURE_STORAGE_CONN_STRING = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT_NAME};AccountKey={AZURE_STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONN_STRING)

    return blob_service_client

def load_to_blob(files):
    blob_service_client = init_blob() 
    uploaded_files = []

    for file in files:
        file_name = file.name
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_STORAGE_CONTAINER_NAME,
            blob=file_name
        )
        try:
            blob_client.upload_blob(file, overwrite=True)  
            print(f"File '{file_name}' uploaded successfully.")
            uploaded_files.append(file_name)
        except Exception as e:
            print(f"Error occurred while uploading the file '{file_name}': {e}")

    return uploaded_files

def convert_to_bytes(blob_names):
    raw_docs = []
    blob_service_client = init_blob()
    
    for blob_name in blob_names:
        try:
            blob_data = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=blob_name).download_blob().readall()
            raw_docs.append({'blob_name': blob_name, 'content': io.BytesIO(blob_data)})

        except Exception as e:
            print(f"Error occurred while downloading the blob '{blob_name}': {e}")
    
    return raw_docs

