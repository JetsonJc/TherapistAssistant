import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from setting.settings import (
    AZURE_STORAGE_CONNECTION_STRING,
    AZURE_STORAGE_KEY,
    AZURE_CONTAINER,
)

def post_document(path, document):
    try:
        connect_str = AZURE_STORAGE_CONNECTION_STRING
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        # Create a unique name for the container
        container_name = AZURE_CONTAINER
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=path)        
        # Upload the created file
        document.seek(0)
        blob_client.upload_blob(document.read())
    except Exception as ex:
        print('Exception:')
        print(ex)