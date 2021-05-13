import os, uuid
import base64
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
        blob_data = blob_client.download_blob()
        filem = blob_data.content_as_text(encoding='utf-8')
        print("dir..............",dir(filem))
        print("tipo.....",type(filem))
        import io
        buffer = io.BytesIO()
        #print(buffer)
        #print("dirbuffer...",dir(buffer))

        ##blob_data.readinto(buffer)
        #with buffer as my_blob:
        #    blob_data = blob_client.download_blob()
        #    blob_data.readinto(my_blob)
        #print(buffer)
        #print("toooodd...",dir(blob_data))
        ##print("intoooo...",dir(filem))
        #print("valor.....",dir(buffer))
        #k = open(buffer.getvalue(), 'r')
        #print(k)


        #base64_encoded_data = base64.b64encode(filem)
        ##base64_file = base64_encoded_data.decode('utf-8')
        #buffer.write(base64_encoded_data)
        #content = buffer.getvalue()
        #buffer.close()
        return filem
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
