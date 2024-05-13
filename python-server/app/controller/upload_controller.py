import os
from flask import jsonify, request
from werkzeug.utils import secure_filename #pip install Werkzeug
from werkzeug.datastructures import ImmutableMultiDict
import uuid
from utils.config import *
from utils.folder_manager import FolderManager
from utils.command_runner import CommandRunner

UPLOAD_FOLDER = 'static/installedImages'  # Define the directory to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS) or is_valid_filename(filename)

def is_valid_filename(filename):
    parts = filename.split('~!~')
    if len(parts) == 2:
        # Check if the first part is a valid UUID
        try:
            uuid.UUID(parts[0], version=4)
            # Check if the second part is a valid operation type
            if parts[1] in {'blurring', 'edge_detection', 'other_operation'}:  # Add more operation types if needed
                return True
        except ValueError:
            pass
    return False

def run_mpi(folder_name):
    command_runner = CommandRunner(PATH_OF_MPI_CODE)
    complex = command_runner.run_mpi_command([folder_name])
    print("this is the complex")



def upload_file():
    
    
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({
            "message": 'No file part in the request',
            "status": 'failed'
        })
        resp.status_code = 400
        return resp
    
   
  
    files = request.files.getlist('files[]')
    print("this is the files ", files)
    errors = {}
    success = False

    print("this is the files " , files)
    
    folder_manager= FolderManager(PATH_OF_SHARED_FOLDER);
    folder_name = str(uuid.uuid4())
    path_of_new_folder = folder_manager.create_folder_with_uuid(folder_name);
    folder_manager.create_result_folder(folder_name)
    print(path_of_new_folder)

    operation_type = "";
    for file in files:      
        if file and allowed_file(file.filename):
            if len(operation_type) is 0:
               temp_file_name = file.filename
               _, operation_type = temp_file_name.split('~!~')

            print("filename is " , file.filename)
            print("operation type is " , operation_type)
            print("the path is " , path_of_new_folder)
            print("folder name is " , folder_name)
            print(path_of_new_folder + file.filename)
            file.save(path_of_new_folder + file.filename)
            success = True
        else:
            resp = jsonify({
                "message": 'File type is not allowed',
                "status": 'failed'
            })
            return resp
    
    #run_mpi(path_of_new_folder)

    if success:
        resp = jsonify({
            "message": 'Files successfully uploaded',
            "status": 'successs'
        })
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({
            "message": 'Failed to upload files',
            "status": 'failed'
        })
        resp.status_code = 500
        return resp

def hello():
    run_mpi("8b43ff96-691d-48ef-8150-ba1162f9e3f4")
    return jsonify({"message": "Hello, upload successful!"})
