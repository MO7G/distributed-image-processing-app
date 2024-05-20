# Distributed Image Processing System using Cloud Computing
This project is a Distributed Image Processing System that leverages cloud computing technologies to efficiently process images. The system allows users to upload images and perform various image processing operations such as filtering, edge detection, and color manipulation. The processing tasks are distributed across multiple virtual machines in the cloud, ensuring scalability and fault tolerance.
Features

## Distributed Processing: The system distributes image processing tasks across multiple virtual machines in the cloud, enabling parallel processing and improving performance.
Scalability: The system is designed to scale by allowing the addition of more virtual machines as the workload increases.
Fault Tolerance: The system implements mechanisms to detect and recover from node failures, reallocating tasks to operational nodes.
Image Processing Algorithms: The system includes various image processing algorithms such as filtering, edge detection, and color manipulation.
User Interface: The system provides a user-friendly interface for uploading images, selecting processing operations, monitoring progress, and downloading processed images.

## Technologies Used

Python
OpenCV
MPI (Message Passing Interface) or OpenCL (Open Computing Language)
AWS (Amazon Web Services)

## Getting Started

### cloud service 

The system includes a cloud web application that can be accessed from anywhere using the following IP address: `http://34.229.138.128/` This web application provides a user-friendly interface for interacting with the Distributed Image Processing System.

### localhost service 

Clone the repository: `git clone https://github.com/your-username/distributed-image-processing.git`
Install the required dependencies: `pip install -r requirements.txt`
Configure your AWS credentials and settings.
Run the main script: `python main.py`

## Usage

Upload images through the user interface.
Select the desired image processing operation.
Monitor the progress of your tasks.
Download the processed images once the operation is complete.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.
## License
This project is licensed under the MIT License.
## Acknowledgments

OpenCV
MPI4Py
AWS Documentation

Project video Description : [Demo](https://youtu.be/3gp-jhw9ee4?si=FrnxlsihC9BbmwCA)

