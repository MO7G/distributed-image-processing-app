import json
import os

class TaskFileManager:
    def __init__(self, base_path="/home/mohd/Desktop/sharedFolder"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def write_task_to_file(self, task, file_name):
        file_path = os.path.join(self.base_path, file_name)
        with open(file_path, "w") as file:
            serialized_task = json.dumps(task)
            file.write(serialized_task)

    def read_task_from_file(self, file_name):
        file_path = os.path.join(self.base_path, file_name)
        with open(file_path, "r") as file:
            serialized_task = file.read()
            return json.loads(serialized_task)

# Example usage:
task = {
    "imageArrayUUID": "04a89561-c8aa-400c-ae81-37dd8a806596",
    "images": [
        {
            "id": "306362b1-26ba-45f1-8a1d-f95935769a0f_istockphoto-1933752815-170667a.webp",
            "imgUrl": "https://19p1472-dis-images.s3.eu-north-1.amazonaws.com/306362b1-26ba-45f1-8a1d-f95935769a0f_istockphoto-1933752815-170667a.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAZI2LB5JHNWBKCKBL%2F20240512%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20240512T122734Z&X-Amz-Expires=3600&X-Amz-Signature=11848ea1bd25e8e15182c5975226dc8adca12e7899b16df8de3f796cc7ffb5ed&X-Amz-SignedHeaders=host&x-id=GetObject",
            "mimeType": "image/webp"
        }
    ]
}

# Create an instance of TaskFileManager with the default base path
task_manager_default = TaskFileManager()

# Write the task to a file using the default base path
task_manager_default.write_task_to_file(task, "task_default.json")

# Read the task from the file using the default base path
read_task_default = task_manager_default.read_task_from_file("task_default.json")
print("Read task from file (default path):", read_task_default)

# Create an instance of TaskFileManager with a custom base path
custom_base_path = "/path/to/custom/folder"
task_manager_custom = TaskFileManager(custom_base_path)

# Write the task to a file using the custom base path
task_manager_custom.write_task_to_file(task, "task_custom.json")

# Read the task from the file using the custom base path
read_task_custom = task_manager_custom.read_task_from_file("task_custom.json")
print("Read task from file (custom path):", read_task_custom)
