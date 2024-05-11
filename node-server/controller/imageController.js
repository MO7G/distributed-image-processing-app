import { PutObjectCommand } from "@aws-sdk/client-s3";
import s3 from "../utils/s3.js";
import { v4 as uuidv4 } from 'uuid';

const sampleFunction = async (req, res) => {
    try {
        // Check if files were uploaded
        if (!req.files || req.files.length === 0) {
            return res.status(400).json({ message: 'No files uploaded' });
        }

        // Iterate through the array of uploaded files
        for (const file of req.files) {
            // Generate a UUID to add to the file name
            const uuid = uuidv4();
            const fileNameWithUuid = `${uuid}_${file.originalname}`;

            const params = {
                Bucket: process.env.BUCKET_NAME,
                Key: fileNameWithUuid, // Use the generated file name
                Body: file.buffer,
                ContentType: file.mimetype,
            };

            // Create a new PutObjectCommand
            const command = new PutObjectCommand(params);

            // Send the command to upload the file
            await s3.send(command);
        }

        // Send success response after all files are uploaded
        res.status(200).json({ message: 'Your images uploaded successfully' });
    } catch (error) {
        console.error("Error uploading files:", error);
        res.status(500).json({ message: 'Internal server error' });
    }
};

export { sampleFunction };
