import { S3Client } from "@aws-sdk/client-s3";

// Load environment variables from .env file
import dotenv from 'dotenv';
dotenv.config();

// Create an S3 client instance
let s3;

try {
    s3 = new S3Client({
        credentials: {
            accessKeyId: process.env.ACCESS_KEY,
            secretAccessKey: process.env.SECRET_ACCESS_KEY
        },
        region: process.env.BUCKET_REGION,
    });
    console.log("s3 bucket connected Successfuly")
} catch (error) {
    console.error("Error initializing S3 client:", error);
}

export default s3;
