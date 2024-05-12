import { PutObjectCommand , GetObjectCommand } from "@aws-sdk/client-s3";
import s3 from "../utils/s3.js";
import { v4 as uuidv4 } from 'uuid';
import publishTask from "../utils/mq.js";
import {getSignedUrl} from "@aws-sdk/s3-request-presigner";
import sessionStore from '../utils/sessionStore.js';
import { Server } from "socket.io";
import { createServer } from "http";




const createImageObject = (uploadedFiles) => {
    const imageArrayUUID = uuidv4();
    const imageObjects = uploadedFiles.map((file) => {
        return {
            id: file.id,
            imgUrl: file.imgUrl,
            mimeType: file.mimeType
        };
    });

    return {
        imageArrayUUID: imageArrayUUID,
        images: imageObjects
    };
};

const sampleFunction = async (req, res) => {
    try {
        // Check if files were uploaded
        if (!req.files || req.files.length === 0) {
            return res.status(400).json({ message: 'No files uploaded' });
        }
        
        const uploadedFiles = req.files.map(file => ({
            id: `${uuidv4()}_${file.originalname}`,
            buffer: file.buffer,
            mimeType: file.mimetype
        }));

        const uploadedFileObject = [];

        // Iterate through the array of uploaded files
        for (const file of uploadedFiles) {
            const PutObjectCommandParams = {
                Bucket: process.env.BUCKET_NAME,
                Key: file.id,
                Body: file.buffer,
                ContentType: file.mimeType,
            };

            // Create a new PutObjectCommand
            let command = new PutObjectCommand(PutObjectCommandParams);
            // Send the command to upload the file
            await s3.send(command);

            const GetObjectCommandParams = {
                Bucket: process.env.BUCKET_NAME,
                Key: file.id,
            };

            command = new GetObjectCommand(GetObjectCommandParams)
            const signedUrl = await getSignedUrl(s3, command, { expiresIn: 3600 });

            const imageObj = {
                id: file.id,
                imgUrl: signedUrl,
                mimeType: file.mimeType,
            }

            uploadedFileObject.push(imageObj);
        }

        // Create the image object after all files are uploaded
        const finalImageObject = createImageObject(uploadedFileObject);

        // Publish the uploaded file URLs to RabbitMQ
        await publishTask(finalImageObject);

        // Send success response after all files are uploaded and tasks are published
        res.status(200).json({ message: 'Your images uploaded successfully', imageObject: finalImageObject });
    } catch (error) {
        console.error("Error uploading files:", error);
        res.status(500).json({ message: 'Internal server error' });
    }
};








export { sampleFunction };