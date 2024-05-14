import React, { useState, useEffect } from "react";
import 'ldrs/ring'
import { zoomies } from 'ldrs'
import { newtonsCradle } from 'ldrs'


// Default values shown

// Default values shown

const ImagesComponent = ({ imagesProp }) => {
  const [images, setImages] = useState([]);
  const [downloadEnabledMap, setDownloadEnabledMap] = useState({});
  newtonsCradle.register()

  useEffect(() => {
    if (Array.isArray(imagesProp)) {
      // Update images state with imagesProp
      setImages(imagesProp);

      // Initialize downloadEnabledMap with false for each image ID
      const initialDownloadEnabledMap = {};
      imagesProp.forEach(image => {
        initialDownloadEnabledMap[image.id] = false;
      });
      setDownloadEnabledMap(initialDownloadEnabledMap);
    }
  }, [imagesProp]);

  const handlePrint = () => {
    console.log("this is the image state ", imagesProp);
  };

  const handleDownload = async (imageId) => {
    // Find the image object with the corresponding ID
    const image = images.find(img => img.id === imageId);
  
    if (!image) {
      console.error("Image not found");
      return;
    }
  
    try {
      // If the image URL is available, initiate download
      if (image.imageURL) {
        // Create a new anchor element
        const link = document.createElement('a');
        link.href = image.imageURL;
        link.setAttribute('download', `image_${imageId}`); // Set the download attribute
  
        // Simulate a click on the anchor element
        document.body.appendChild(link);
        link.click();
  
        // Remove the anchor element from the DOM
        document.body.removeChild(link);
      } else {
        // If the image is from a file input, initiate download using Blob
        const blob = new Blob([image.file]);
        const url = URL.createObjectURL(blob);
  
        // Create a new anchor element
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `image_${imageId}`); // Set the download attribute
  
        // Simulate a click on the anchor element
        document.body.appendChild(link);
        link.click();
  
        // Remove the anchor element and revoke the Blob URL
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error("Error downloading image:", error);
    }
  };
  
  return (
    <div className="container pt-4">
      <div className="row">
        <div className="col-lg-12">
          <div className="card shadow">
            <div className="card-header">
              <h4 className="card-title fw-bold">Images List</h4>
            </div>
            <div className="card-body">
              <div className="row">
                {images.map((image, index) => (
                  <div key={index} className="col-lg-3 mb-3">
                    {/* Conditional rendering based on imageURL */}
                    <div style={{ position: "relative", width: "100%", height: "auto", marginBottom: "100px" }}>
                      {image.imageURL ? (
                        <>
                          <img
                            src={image.imageURL}
                            alt={`Image ${index}`}
                            style={{ width: "100%", height: "auto" }}
                          />
                          <button
                            onClick={() => handleDownload(image.id)}
                            className="btn btn-primary"
                            style={{ position: "absolute", bottom: "10px", left: "50%", transform: "translateX(-50%)" }}
                          >
                            Download
                          </button>
                        </>
                      ) : (
                        <img
                          src={URL.createObjectURL(image.file)}
                          alt={`Image ${index}`}
                          style={{ width: "100%", height: "auto" }}
                        />
                      )}
                      {/* Conditional rendering of spinner */}
                      {!image.imageURL && (
                        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", width: "100%", height: "100%", marginTop: "30px" }}>
                          <div style={{ display: "flex", justifyContent: "center", alignItems: "center", width: "100%", height: "100%" }}>
                            <l-newtons-cradle
                              size="78"
                              speed="1.4"
                              color="black"
                            ></l-newtons-cradle>

                          </div>

                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ImagesComponent;
