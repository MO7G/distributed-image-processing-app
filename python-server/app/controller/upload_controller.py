import os
from flask import jsonify, request
from werkzeug.utils import secure_filename #pip install Werkzeug

UPLOAD_FOLDER = 'static/installedImages'  # Define the directory to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    print("from here")
    print(request.files)
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({
            "message": 'No file part in the request',
            "status": 'failed'
        })
        resp.status_code = 400
        return resp
    
    print("downhereee")
  
    files = request.files.getlist('files[]')
    print("this is the files ", files)
    errors = {}
    success = False
    
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("this si the file name " , filename)
            path = '/home/mohd/working/distributed-image-processing-app/python-server/app/static/installedImages/'+filename;
            file.save(path)
            success = True
        else:
            resp = jsonify({
                "message": 'File type is not allowed',
                "status": 'failed'
            })
            return resp
         
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
    return jsonify({"message": "Hello, upload successful!"})
