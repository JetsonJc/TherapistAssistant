import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from rest_framework.exceptions import ValidationError
from setting.settings import (
    AZURE_STORAGE_CONNECTION_STRING,
    AZURE_STORAGE_KEY,
    AZURE_CONTAINER,
)

def post_document(name, document):
    try:
        name_document = document._get_name()
        file_data = os.path.splitext(name_document)
        extension = file_data[1]
        path_complete = name + extension

        connect_str = AZURE_STORAGE_CONNECTION_STRING
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        # Create a unique name for the container
        container_name = AZURE_CONTAINER
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=path_complete)
        # Upload the created file
        document.seek(0)
        blob_client.upload_blob(document.read())
        return path_complete
    except Exception as ex:
        print('Exception:')
        print(ex)
        raise ValidationError(ex)


def get_document(path):
    try:
        connect_str = AZURE_STORAGE_CONNECTION_STRING
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the container
        container_name = AZURE_CONTAINER

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=path)

        content = blob_client.download_blob().readall()

        return content
    except Exception as ex:
        print('Exception.....:')
        print(ex)
        raise ValidationError(ex)


def delete_document(path):
    try:
        connect_str = AZURE_STORAGE_CONNECTION_STRING
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        # Create a unique name for the container
        container_name = AZURE_CONTAINER
        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=path)
        # Delete
        blob_client.delete_blob()
        return True
    except Exception as ex:
        print('Exception:')
        print(ex)
        raise ValidationError(ex)
