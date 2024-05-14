from folder_manager import FolderNavigator
from s3_manager import S3FileManager;

folder_nav = FolderNavigator();
s3 = S3FileManager()


images_with_url = {}
list = folder_nav.list_files_in_folder_results("404cc357-c42d-4180-87aa-39ffd36ac842")
for image in list:
    s3.upload_image("404cc357-c42d-4180-87aa-39ffd36ac842" + "/" +"result/" + image ,image)
    link = s3.generate_presigned_url(image)
    images_with_url[image] = link



