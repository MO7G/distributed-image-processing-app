import React, { useState, useRef } from "react";
import axios from "axios";
import ImagesComponent from "../Images/images";

const ImageUpload = () => {
  const [image, setImage] = useState("");
  const [selectedOption, setSelectedOption] = useState(""); // State to hold the selected option
  const [responseMsg, setResponseMsg] = useState({
    status: "",
    message: "",
    error: "",
  });
  const [fileError, setFileError] = useState(""); // State to hold file selection error

  const handleChange = (e) => {
    const imagesArray = [];
    for (let i = 0; i < e.target.files.length; i++) {
      fileValidate(e.target.files[i]);
      imagesArray.push(e.target.files[i]);
    }
    setImage(imagesArray);
  };

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value); // Update selected option state
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
      data.append("files[]", image[i]);
    }

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
              <option value="">Select...</option>
              <option value="x">Option X</option>
              <option value="y">Option Y</option>
              <option value="z">Option Z</option>
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
    </div>
  );
};

export default ImageUpload;
