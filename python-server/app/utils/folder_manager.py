import os
import uuid
import os
import stat
import datetime
import time
from utils.config import PATH_OF_SHARED_FOLDER
class FolderManager:
    def __init__(self, base_path=None):
        if base_path is None:
            self.base_path = PATH_OF_SHARED_FOLDER
        else:
            self.base_path = base_path
        self.delete_time_for_content = 60 * 5

    def create_folder_with_uuid(self, folder_uuid=None):
        if folder_uuid is None:
            folder_uuid = str(uuid.uuid4())
        
        folder_path = os.path.join(self.base_path, folder_uuid)
        os.makedirs(folder_path)

        return folder_path + '/'

    def create_result_folder(self, folder_uuid):
        
        folder_path = os.path.join(self.base_path, folder_uuid,"result")
        os.makedirs(folder_path)

    def delete_folder_with_uuid(self, folder_uuid):
        folder_path = os.path.join(self.base_path, folder_uuid)
        
        if os.path.exists(folder_path):
            self._delete_folder_recursive(folder_path)
            print("Folder deleted successfully.")
        else:
            print("Folder does not exist.")

    def _delete_folder_recursive(self, folder_path):
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
    
    # consider if the folder is being modified as well not implemented rn 
    def clean_downloaded_images_folder(self):
        path = self.base_path
    
        # Check if the path is a directory
        if not os.path.isdir(path):
            print("Invalid directory path.")
            return
    
        # Iterate through the files and folders
        for item in os.listdir(path):
            # Join the item with the path to get the full path
            full_path = os.path.join(path, item)
    
            # Get metadata
            metadata = os.stat(full_path)
    
            # Check if it's a directory
            if os.path.isdir(full_path):
                # Check last access time of the folder
                last_access_time = os.path.getatime(full_path)
                current_time = time.time()
                time_difference = current_time - last_access_time

                if time_difference > self.delete_time_for_content:  
                    self._delete_folder_recursive(full_path)
                    print("Folder deleted due to inactivity.")
                else:
                    print("Folder has been accessed recently, not deleting.")

            else:
                # no deletion for files for now 
                print("File:", item)
                print("Size:", metadata.st_size, "bytes")
                print("Last Modified:", datetime.datetime.fromtimestamp(metadata.st_mtime))
                print("Permissions:", oct(stat.S_IMODE(metadata.st_mode)))

            print("----------")
            print("----------")

    def temp(self):
        print("hasfadsf")
        
    
    


class FolderNavigator:
    def __init__(self):
        self.another_path = PATH_OF_SHARED_FOLDER

    def navigate_to_folder(self, folder_name):
        folder_path = os.path.join(self.current_path, folder_name)
        if os.path.isdir(folder_path):
            self.current_path = folder_path
            return True
        else:
            print(f"The folder '{folder_name}' does not exist in the current directory.")
            return False

    def list_files_in_folder_results(self, folder_name):
        dist_folder = os.path.join(self.another_path, folder_name + "/result/" )

        # Get list of files in the specified folder, excluding the current file
        current_file_name = os.path.basename(__file__)  # Assuming __file__ contains the name of the current file
        files = [f for f in os.listdir(dist_folder) if os.path.isfile(os.path.join(dist_folder, f)) and f != current_file_name]
        #list_without_extension = [filename.split(".png")[0] for filename in files]
        #return list_without_extension
        return files

