import os
import uuid

class FolderManager:
    def __init__(self, base_path=None):
        if base_path is None:
            self.base_path = "/home/mohd/Desktop/sharedFolder/DownloadedImages/"
        else:
            self.base_path = base_path

    def create_folder_with_uuid(self, folder_uuid=None):
        if folder_uuid is None:
            folder_uuid = str(uuid.uuid4())
        
        folder_path = os.path.join(self.base_path, folder_uuid)
        os.makedirs(folder_path)

        return folder_path + '/'

    def delete_folder_with_uuid(self, folder_uuid):
        folder_path = os.path.join(self.base_path, folder_uuid)
        
        if os.path.exists(folder_path):
            self._delete_folder_recursive(folder_path)
            print("Folder deleted successfully.")
        else:
            print("Folder does not exist.")

    def _delete_folder_recursive(self, folder_name):
        folder_path = os.path.join(self.base_path, folder_name)
        print(folder_path)
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for file in files:
                   os.remove(os.path.join(root, file))
                for dir in dirs:
                   os.rmdir(os.path.join(root, dir))
            os.rmdir(folder_path)
            print("Folder deleted successfully.")
        else:
            print("Folder does not exist.")

    def list_folders(self):
        folders = []
        for entry in os.listdir(self.base_path):
            entry_path = os.path.join(self.base_path, entry)
            if os.path.isdir(entry_path):
                folders.append(entry)
        return folders
    
