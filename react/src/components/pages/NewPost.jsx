import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';

const backendURL = 'http://localhost:8080'; // Replace with your backend server URL

export default function NewPost() {
  const [files, setFiles] = useState([]);
  const [captions, setCaptions] = useState([]);
  const [uploadProgress, setUploadProgress] = useState({});
  const [socket, setSocket] = useState(null); // Track socket connection

  const openSocketConnection = () => {
    if (!socket) {
      const newSocket = io(backendURL, { withCredentials: false });
      setSocket(newSocket);
      
      // Listen for a response event from the server
      newSocket.on("connection", (data) => {
        // Handle the response from the server
        console.log("Image processed:", data);
        // You can navigate or perform other actions based on the response
      });


      // Listen for a response event from the server
      newSocket.on("message", (data) => {
        // Handle the response from the server
        console.log("message from server is:", data);
        // You can navigate or perform other actions based on the response
      });
    } else {
      console.log("Socket connection already established");
    }
  };
  

  const handleCloseSocket = () => {
    if (socket) {
      // Close the socket connection
      socket.disconnect();
      setSocket(null);
    } else {
      console.log("Socket is already closed");
    }
  };

  const submit = async (event) => {
    event.preventDefault();
  
    if (files.length === 0) {
      console.error("No files selected");
      return;
    }
  
    const formData = new FormData();
  
    files.forEach((file, index) => {
      formData.append("images", file);
      formData.append("captions", captions[index]);
    });
  
    try {
      await axios.post(`${backendURL}/api/images`, formData)
        .then((response) => {
          // Handle successful response
          console.log('Images uploaded successfully!');
          console.log("Backend response:", response.data); // Access data from response
          openSocketConnection(); // Open socket connection upon successful post request
        });
    } catch (error) {
      // Display error message
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
      <div className="flex flex-col items-center justify-center">
      <button onClick={openSocketConnection}>Connect to Socket</button>
      <button onClick={handleCloseSocket}>Close  Socket</button>

      {/* Rest of the form and UI */}
    </div>
    </div>
  );
}
