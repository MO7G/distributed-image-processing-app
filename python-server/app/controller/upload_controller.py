import os
from flask import jsonify, request
from werkzeug.utils import secure_filename #pip install Werkzeug
from werkzeug.datastructures import ImmutableMultiDict
import uuid
from utils.config import *
from utils.folder_manager import FolderManager
from scripts.python_subprocess import run_command_with_subprocess
from utils.s3_manager import S3FileManager
from utils.folder_manager import FolderNavigator
s3 = S3FileManager()

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
            if parts[1] in {'color_inversion', 'edge_detection', 'increase_brightness'}:  # Add more operation types if needed
                return True
        except ValueError:
            pass
    return False

def upload_to_s3(folder_name , ):
    folder_nav = FolderNavigator();

    print("okay this is me " , folder_name)
    images_with_url = {}

    list = folder_nav.list_files_in_folder_results(folder_name)
    for image in list:
       s3.upload_image(folder_name + "/" +"result/" + image ,image)
       link = s3.generate_presigned_url(image)
       images_with_url[image] = link

    return images_with_url;

   


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
    errors = {}
    success = False

    folder_manager= FolderManager(PATH_OF_SHARED_FOLDER);
    folder_name = str(uuid.uuid4())
    path_of_new_folder = folder_manager.create_folder_with_uuid(folder_name);
    folder_manager.create_result_folder(folder_name)
    print(path_of_new_folder)

    operation_type = "";
    for file in files:      
        if file and allowed_file(file.filename):
            if len(operation_type) == 0:
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
    
    run_command_with_subprocess(folder_name, operation_type);
    result = upload_to_s3(folder_name);

    if success:
        resp = jsonify({
            "message": 'Files successfully uploaded',
            "status": 'success',
            "result" : result
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

