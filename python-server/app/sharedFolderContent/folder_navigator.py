import os
import netifaces as ni

class FolderNavigator:
    def __init__(self):
        self.current_path = os.getcwd() + '/DownloadedImages/'
        self.another_path = os.path.dirname(os.path.abspath(__file__)) + '/DownloadedImages/'

    def navigate_to_folder(self, folder_name):
        folder_path = os.path.join(self.current_path, folder_name)
        if os.path.isdir(folder_path):
            self.current_path = folder_path
            return True
        else:
            print(f"The folder '{folder_name}' does not exist in the current directory.")
            return False

    def list_files_in_folder(self, folder_name):

        dist_folder = os.path.join(self.another_path, folder_name)
        
        print(dist_folder)
        
        # Get list of files in the specified folder, excluding the current file
        current_file_name = os.path.basename(__file__)  # Assuming __file__ contains the name of the current file
        files = [f for f in os.listdir(dist_folder) if os.path.isfile(os.path.join(dist_folder, f)) and f != current_file_name]
        return files

