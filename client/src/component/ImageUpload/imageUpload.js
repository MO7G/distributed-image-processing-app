import React, { useState, useRef } from "react";
import axios from "axios";
import ImagesComponent from "../Images/images";
import { v4 as uuidv4 } from 'uuid';
import { zoomies } from 'ldrs'



// Default values shown

const ImageUpload = () => {
  zoomies.register()
  const [image, setImage] = useState("");
  const [selectedOption, setSelectedOption] = useState("edge_detection"); // State to hold the selected option
  const [responseMsg, setResponseMsg] = useState({
    status: "",
    message: "",
    error: "",
  });
  const [clearActive , setClearActive] = useState(true)
  const [flagStartUpload, setFlagStartUpload] = useState(false)
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
    setClearActive(false)
    setFlagStartUpload(true);
    // Check if no files are selected
    if (image.length === 0) {
      setFileError("Please select at least one file to upload.");
      setFlagStartUpload(false); // Set flag to false here too
      return;
    }
  
    const data = new FormData();
    for (let i = 0; i < image.length; i++) {
      data.append("files[]", image[i].file);
    }
  
    axios.post("http://127.0.0.1:5000/upload", data)
      .then((response) => {
        if (response.status === 201) {
          setResponseMsg({
            status: response.data.status,
            message: response.data.message,
          });
  
          console.log("this sithe reuslt ", response.data.result);
          // Update the state to include the image URLs received from the backend response
          const updatedImages = image.map((imageItem) => {
            // Assuming response.data.result contains the URLs as provided in the backend response
            const imageURL = response.data.result[imageItem.id + '.png'];
            // Just set the imageURL directly to the imageItem
            return { ...imageItem, imageURL };
          });
  
          setImage(updatedImages);
        }
        setFlagStartUpload(false);
        setClearActive(true) // Set flag to false in the then block
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
        setFlagStartUpload(false); // Set flag to false in the catch block
      });
  };
  
  const handleClear = () => {
    // Clear the selected images
    setImage([]);
    // Reset the selected option to its default value
    setSelectedOption("edge_detection");
    // Reset the file input field
    const fileInput = document.getElementById("images");
    if (fileInput) {
      fileInput.value = "";
    }
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
            <select className="form-select" id="options" value={selectedOption} onChange={handleOptionChange} disabled={image.length === 0 || flagStartUpload}>
              <option value="edge_detection">edge_detection</option>
              <option value="color_inversion">color inversion</option>
              <option value="increase_brightness">increase brightness</option>
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

              <div className="card-footer d-flex justify-content-between align-items-center">
                <div>
                  {flagStartUpload && (
                    <l-zoomies
                      size="700"
                      stroke="5"
                      bg-opacity="0.1"
                      speed="2.4"
                      color="black"
                    ></l-zoomies>
                  )}
                  {clearActive && (
                    <>
                     <button disabled={flagStartUpload} onClick={handleClear}  className="btn btn-danger">
                    Clear
                  </button>
                    </>
                  )}
                </div>
                <div>
                  <button disabled={flagStartUpload} type="submit" className="btn btn-success">
                    Upload
                  </button>
                </div>
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
      <ImagesComponent imagesProp={image} flagStartUploadProps={flagStartUpload} ref={childRef} />
    </div>
  );
};

export default ImageUpload;
