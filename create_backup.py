"""
    Author: Siddharth Gupta
    email: gsiddharth47@gmail.com
    OS: Ubuntu 24.04
"""

import os
import sys
import tarfile
from google.cloud import storage


# The code requires GCP application default credentials to be set beforehand and please install google cloud storage 
# python module

def gcp_upload(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def tar_directory(directory_path, output_tar):
    if not os.listdir(directory_path):
        print(f"Directory '{directory_path}' is empty. Can't create backup of an empty dir...")
        return

    with tarfile.open(output_tar, "w") as tar:
        tar.add(directory_path, arcname=os.path.basename(directory_path))
    print(f"{directory_path} compressed to tar archive successfully")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python create-backup.py <directory_path> <output_tar>")
        sys.exit(1)

    directory_to_tar = sys.argv[1]
    output_tar_file = sys.argv[2]
    tar_directory(directory_to_tar, output_tar_file)
    gcp_upload('sid-qa-bucket-2', output_tar_file, output_tar_file)
