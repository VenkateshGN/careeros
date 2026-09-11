import os

class StorageService:
    def __init__(self):
        # Mock S3 Initialization
        try:
            import boto3
            self.s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "mock"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "mock")
            )
        except Exception:
            self.s3 = None
        self.bucket = os.getenv("S3_BUCKET_NAME", "mock-careeros-bucket")

    def upload_file(self, file_content: bytes, destination_key: str):
        print(f"Mock Uploaded file to s3://{self.bucket}/{destination_key}")
        return f"https://mock-s3-url/{self.bucket}/{destination_key}"

    def get_file_url(self, key: str):
        return f"https://mock-s3-url/{self.bucket}/{key}"

storage_service = StorageService()
