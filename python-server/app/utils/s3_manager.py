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

            print(folder_name)
            print(s3_key)
            local_image_path = os.path.join(self.upload_directory, folder_name, s3_key)
            print(local_image_path)
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

# Example usage:
s3_file_manager = S3FileManager()

# Upload image to S3
#local_image_path = "/home/mohd/Desktop/sharedFolder/temp/image.jpg"
s3_key = "haha.jpg"
#s3_file_manager.upload_image(local_image_path, s3_key)

# Download image from S3
#s3_file_manager.download_image(s3_key)
s3_file_manager.download_image("man",s3_key)
