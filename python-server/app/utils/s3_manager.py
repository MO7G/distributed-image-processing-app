import boto3
import os
from dotenv import load_dotenv

class S3FileManager:
    def __init__(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            env_file_path = os.path.join(script_dir, '.env')
            load_dotenv(dotenv_path=env_file_path)
            self.access_key = os.getenv('ACCESS_KEY')
            self.secret_access_key = os.getenv('SECRET_ACCESS_KEY')
            self.bucket_region = os.getenv('BUCKET_REGION')
            self.bucket_name = os.getenv('BUCKET_NAME')
            self.download_directory = "/home/mohd/Desktop/sharedFolder/DownloadedImages/"
            self.upload_directory = "/home/mohd/Desktop/sharedFolder/DownloadedImages/"
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.bucket_region
            )
            print("Connected to S3 successfully")
        except Exception as e:
            print(f"Error connecting to S3: {e}")

    def upload_image(self,folder_name , s3_key):
        try:
            local_image_path = os.path.join(self.upload_directory, folder_name)
            self.s3.upload_file(local_image_path, self.bucket_name, s3_key)
            print(f"Image uploaded successfully to S3 with key: {s3_key}")
        except Exception as e:
            print(f"Error uploading image to S3: {e}")

    def download_image(self,folder_name , s3_key):
        try:
            filename = os.path.basename(s3_key)
            downloaded_image_path = os.path.join(self.download_directory, folder_name,filename)
            print("hahaha" , downloaded_image_path)
            self.s3.download_file(self.bucket_name, s3_key, downloaded_image_path)
            print(f"Image downloaded successfully to: {downloaded_image_path}")
        except Exception as e:
            print(f"Error downloading image from S3: {e}")

    def generate_presigned_url(self, object_key, expiration_time=3600):
        """
        Generate a presigned URL for accessing an S3 object.

        :param object_key: Key of the S3 object.
        :param expiration_time: Expiration time of the presigned URL in seconds (default: 3600 seconds).
        :return: Presigned URL.
        """
        try:
            # Generate the presigned URL
            presigned_url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration_time
            )
            return presigned_url
        except Exception as e:
            print(f"Error generating presigned URL: {e}")

