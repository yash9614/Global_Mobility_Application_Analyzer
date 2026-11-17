from visa.configuration.aws_connection import get_s3_client

class S3Storage:
    def __init__(self):
        self.client = get_s3_client()

    def upload_file(self, local_path, bucket, key):
        self.client.upload_file(local_path, bucket, key)
