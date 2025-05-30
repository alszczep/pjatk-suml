from datetime import datetime, timedelta
import io
import os
import uuid

from azure.storage.blob import BlobSasPermissions, BlobServiceClient, generate_blob_sas

service_client = BlobServiceClient.from_connection_string(
    os.environ["BLOB_CONNECTION_STRING"]
)
model_container_client = service_client.get_container_client("model")
images_container_name = "images"
images_container_client = service_client.get_container_client(images_container_name)


def upload_image_to_blob(file):
    extension = os.path.splitext(file.name)[-1]
    file_name = str(uuid.uuid4()) + extension
    blob_client = images_container_client.get_blob_client(file_name)

    file.seek(0)
    blob_client.upload_blob(file, overwrite=True)

    return blob_client.url


def download_model_from_blob():
    blob_client = model_container_client.get_blob_client("model.keras")
    data = blob_client.download_blob().readall()
    return io.BytesIO(data)


def parse_connection_string(connection_string):
    parts = connection_string.split(";")
    result = {}
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            result[key] = value
    return result


def get_blob_file_url_with_sas_token(file_url):
    blob_name = file_url.split("/")[-1]

    parsed_connection_string = parse_connection_string(
        os.environ["BLOB_CONNECTION_STRING"]
    )
    account_name = parsed_connection_string["AccountName"]
    account_key = parsed_connection_string["AccountKey"]

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=images_container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(minutes=15),
    )
    return f"https://{account_name}.blob.core.windows.net/{images_container_name}/{blob_name}?{sas_token}"
