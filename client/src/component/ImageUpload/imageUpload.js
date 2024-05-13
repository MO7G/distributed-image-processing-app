import React, { useState, useRef } from "react";
import axios from "axios";
import ImagesComponent from "../Images/images";
import { v4 as uuidv4 } from 'uuid';

const ImageUpload = () => {
  const [image, setImage] = useState("");
  const [selectedOption, setSelectedOption] = useState("blurring"); // State to hold the selected option
  const [responseMsg, setResponseMsg] = useState({
    status: "",
    message: "",
    error: "",
  });
  const [fileError, setFileError] = useState(""); // State to hold file selection error
  const delimiter = '~!~';

  const handleChange = (e) => {
    const imagesWithIds = [];
    for (let i = 0; i < e.target.files.length; i++) {
      const file = e.target.files[i];
      const id = uuidv4() + delimiter + selectedOption; // Generate a unique ID for each file
      fileValidate(file);
      const renamedFile = new File([file], id, { type: file.type }); // Create a new File object with the modified name
  
        
      imagesWithIds.push({ id: id, file: renamedFile }); // Push the file object with id to imagesWithIds array
  }
  
    console.log("This is the array of images with IDs", imagesWithIds);
    setImage(imagesWithIds);
};


  

const handleOptionChange = (e) => {
  const newSelectedOption = e.target.value;
  const updatedImages = image.map(image => {
    const [id, currentOperation] = image.id.split('~!~');
      const newId = `${id}~!~${newSelectedOption}`;
      const newFileName = `${id}~!~${newSelectedOption}`;
      const newFile = new File([image.file], newFileName);
      return {
        id: newId,
        file: newFile
      }
  });

  setImage(updatedImages);
  setSelectedOption(newSelectedOption);
};


  const submitHandler = (e) => {
    e.preventDefault();

    // Check if no files are selected
    if (image.length === 0) {
      setFileError("Please select at least one file to upload.");
      return;
    }

    const data = new FormData();
    for (let i = 0; i < image.length; i++) {
      console.log(image[i])
      data.append("files[]", image[i].file);
    }


    console.log("this is the data " , data)
    axios.post("http://127.0.0.1:5000/upload", data)
      .then((response) => {
        if (response.status === 201) {
          setResponseMsg({
            status: response.data.status,
            message: response.data.message,
          });
          setTimeout(() => {
            setImage("");
            setResponseMsg("");
          }, 10000);
          document.querySelector("#imageForm").reset();
          // getting uploaded images
          childRef.current.getImages();
        }
        console.log(response.data.message)
      })
      .catch((error) => {
        console.error(error);
        if (error.response) {
          if (error.response.status === 401) {
            setResponseMsg({
              status: "danger",
              message: "Invalid credentials",
            });
          }
        }
      });
  };

  const fileValidate = (file) => {
    if (
      file.type === "image/png" ||
      file.type === "image/jpg" ||
      file.type === "image/jpeg"
    ) {
      setFileError("");
      return true;
    } else {
      setFileError("File type allowed only jpg, png, jpeg");
      return false;
    }
  };

  const childRef = useRef(null);

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          {/* Options */}
          <div className="mb-3">
            <label htmlFor="options" className="form-label">Select an option:</label>
            <select className="form-select" id="options" value={selectedOption} onChange={handleOptionChange}>
              <option value="blurring">blurring</option>
              <option value="edge_detection">edge_detection</option>
              <option value="other_operation">other_operation</option>
            </select>
          </div>

          {/* Image Upload Form */}
          <form onSubmit={submitHandler} encType="multipart/form-data" id="imageForm">
            <div className="card shadow">
              <div className="card-body">
                <div className="form-group py-2">
                  <label htmlFor="images" className="form-label">Choose Images</label>
                  <input
                    type="file"
                    name="image"
                    multiple
                    onChange={handleChange}
                    className="form-control"
                  />
                  {fileError && <span className="text-danger">{fileError}</span>}
                </div>
              </div>

              <div className="card-footer text-end">
                <button type="submit" className="btn btn-success">
                  Upload
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>

      {/* Response Message */}
      <div className="row justify-content-center mt-4">
        <div className="col-lg-8">
          {responseMsg.status && (
            <div className={`alert alert-${responseMsg.status === "success" ? "success" : "danger"}`}>
              {responseMsg.message}
            </div>
          )}
        </div>
      </div>

      <ImagesComponent imagesProp={image} ref={childRef}/>
      <button onClick={()=>console.log(image)}>dooooo</button>
    </div>
  );
};

export default ImageUpload;
