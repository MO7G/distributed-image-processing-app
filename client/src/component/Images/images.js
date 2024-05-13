import React, { useState, useEffect } from "react";

const ImagesComponent = ({ imagesProp }) => {
  const [images, setImages] = useState([]);
  const [downloadEnabledMap, setDownloadEnabledMap] = useState({}); // Map to track enabled download buttons

  useEffect(() => {
    // Check if imagesProp is an array
    if (Array.isArray(imagesProp)) {
      // Convert each image object to a URL and update images state
      const imageUrls = imagesProp.map(image => ({
        id: image.id,
        url: URL.createObjectURL(image.file)
      }));
      setImages(imageUrls);

      // Initialize downloadEnabledMap with false for each image ID
      const initialDownloadEnabledMap = {};
      imageUrls.forEach(image => {
        initialDownloadEnabledMap[image.id] = false;
      });
      setDownloadEnabledMap(initialDownloadEnabledMap);

      // Cleanup function to revoke the object URLs when component unmounts
      return () => {
        imageUrls.forEach(image => URL.revokeObjectURL(image.url));
      };
    }
  }, [imagesProp]);

  const handlePrint = () => {
    // Just an example of handling images, you can modify this according to your needs
    if (images.length > 0) {
      console.log(images[0]); // Image URL
    }
  };

  const handleDownload = (imageId) => {
    // Perform download logic here
    console.log("Downloading:", imageId);
  };

  const toggleDownload = (imageId) => {
    setDownloadEnabledMap(prevState => ({
      ...prevState,
      [imageId]: !prevState[imageId] // Toggle the state for the specified image ID
    }));
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
                {/* Map over the images array and render an img tag for each image */}
                {images.map((image, index) => (
                  <div key={index} className="col-lg-3 mb-3">
                    <img
                      src={image.url}
                      alt={`Image ${index}`} // Set alt text appropriately
                      style={{ width: "100%", height: "auto" }} // Set image size
                    />
                    {/* Download button */}
                    <button
                      onClick={() => handleDownload(image)}
                      disabled={!downloadEnabledMap[image.id]} // Disable or enable the button based on downloadEnabledMap
                      className="btn btn-primary mt-2"
                    >
                      Download
                    </button>
                    {/* Button to toggle download button for this image */}
                    <button
                      onClick={() => toggleDownload(image.id)}
                      className="btn btn-success mt-2 ms-2"
                    >
                      {downloadEnabledMap[image.id] ? "Disable Download" : "Enable Download"}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
      <button onClick={handlePrint} className="btn btn-secondary me-2">
        Print First Image URL
      </button>
    </div>
  );
}

export default ImagesComponent;
