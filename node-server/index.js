import express from "express"
import imageRoutes from "./routes/imageRoutes.js"
import s3 from "./utils/s3.js";
const app = express();
const port = 8080;

// Middleware
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies

// Routes
app.use('/api/', imageRoutes); // Use image router


// Root route
app.get('/', (req, res) => {
    // Your '/' route logic here
    res.send('Server is up and running!');
});

// Root route middleware for handling other routes
app.use((req, res, next) => {
  // This middleware will only be reached if no other routes match
res.status(404).send('404 - Not Found');
});


// Start server
app.listen(port, () => {
console.log(`Server is running on port ${port}`);
});
