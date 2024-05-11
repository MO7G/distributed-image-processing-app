import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function NewPost() {
  const [files, setFiles] = useState([]);
  const [captions, setCaptions] = useState([]);
  const [uploadProgress, setUploadProgress] = useState({});
  const navigate = useNavigate();

  const submit = async (event) => {
    event.preventDefault();

    // Check if files array is empty
    if (files.length === 0) {
      console.error("No files selected");
      return;
    }

    const formData = new FormData();

    // Append each file and its corresponding caption
    files.forEach((file, index) => {
      formData.append("images", file);
      formData.append("captions", captions[index]);
    });

    try {
      const config = {
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress((prevState) => ({
            ...prevState,
            [file.name]: percentCompleted,
          }));
        },
        headers: { 'Content-Type': 'multipart/form-data' },
      };

      await axios.post("/api/images", formData, config);
      navigate("/"); // Redirect after successful upload
    } catch (error) {
      // Handle errors
      console.error("Error uploading images:", error);
    }
  };

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files);
    setFiles([...files, ...selectedFiles]);

    // Initialize captions for new files
    const newCaptions = captions.concat(selectedFiles.fill(""));
    setCaptions(newCaptions);
  };

  const handleCaptionChange = (event, index) => {
    const newCaptions = [...captions];
    newCaptions[index] = event.target.value;
    setCaptions(newCaptions);
  };

  const removeFile = (index) => {
    const newFiles = [...files];
    const newCaptions = [...captions];

    newFiles.splice(index, 1);
    newCaptions.splice(index, 1);

    setFiles(newFiles);
    setCaptions(newCaptions);
  };

  const FileInput = ({ file, index, progress }) => (
    <div key={index}>
      <div className="flex items-center space-x-2">
        <span>{file.name}</span>
        <button style={{ background: "red" }} onClick={() => removeFile(index)}>Remove</button>
      </div>
      <input value={captions[index] || ""} onChange={(e) => handleCaptionChange(e, index)} type="text" placeholder="Caption" />
      {progress && <progress value={progress} max="100" />}
    </div>
  );

  return (
    <div className="flex flex-col items-center justify-center">
      <form onSubmit={submit} style={{ width: 650 }} className="flex flex-col space-y-5 px-5 py-14">
        {files.map((file, index) => (
          <FileInput key={index} file={file} index={index} progress={uploadProgress[file.name]} />
        ))}
        <input type="file" accept="image/*" onChange={handleFileChange} multiple />
        <button type="submit">Submit</button>
      </form>
      <button onClick={() => console.log(files)}>print</button>
    </div>
  );
}
