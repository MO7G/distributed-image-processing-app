import React, { useState, useEffect } from "react";

const ImagesComponent = ({ imagesProp }) => {
  const [images, setImages] = useState([]);
  const [downloadEnabled, setDownloadEnabled] = useState(false); // State to manage download button

  useEffect(() => {
    // Check if imagesProp is an array
    if (Array.isArray(imagesProp)) {
      // Convert File objects to URLs
      const imageUrls = imagesProp.map(image => URL.createObjectURL(image));
      // Update images state with the URLs
      setImages(imageUrls);

      // Cleanup function to revoke the object URLs when component unmounts
      return () => {
        imageUrls.forEach(url => URL.revokeObjectURL(url));
      };
    }
  }, [imagesProp]);

  const handlePrint = () => {
    // Just an example of handling images, you can modify this according to your needs
    if (images.length > 0) {
      console.log(images[0]); // Image URL
    }
  };

  const handleDownload = (imageUrl) => {
    // Perform download logic here
    console.log("Downloading:", imageUrl);
  };

  // Function to unlock the download button based on some condition
  const unlockDownload = () => {
    // Perform unlocking logic here
    setDownloadEnabled(true);
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
                {images.map((imageUrl, index) => (
                  <div key={index} className="col-lg-3 mb-3">
                    <img
                      src={imageUrl}
                      alt={`Image ${index}`} // Set alt text appropriately
                      style={{ width: "100%", height: "auto" }} // Set image size
                    />
                    {/* Download button, initially disabled */}
                    <button
                      onClick={() => handleDownload(imageUrl)}
                      disabled={!downloadEnabled}
                      className="btn btn-primary mt-2"
                    >
                      Download
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
      <button onClick={unlockDownload} className="btn btn-success">
        Unlock Download
      </button>
    </div>
  );
}

export default ImagesComponent;
