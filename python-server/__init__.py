import os

# Function to dynamically add project root to PYTHONPATH
def add_project_root_to_path():
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(project_root)
    os.environ['PYTHONPATH'] = f"{project_root}:{os.environ.get('PYTHONPATH', '')}"

# Call the function to add project root to PYTHONPATH
add_project_root_to_path()  

import sys

for path in sys.path:
    print(path)
