import express from "express";
import multer from "multer";
import { sampleFunction } from '../controller/imageController.js';

const router = express.Router();

// Configure multer for file upload
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Define route for uploading multiple images
router.post('/images', upload.array("images", 10), sampleFunction);

export default router;
