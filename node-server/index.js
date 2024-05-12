import express from "express";
import http from "http";
import { Server } from "socket.io";
import imageRoutes from "./routes/imageRoutes.js";
import { listenToQueue } from './utils/queueListener.js';
import cors from "cors"; // Import the cors middleware

const app = express();
const port = 8080;

// Middleware
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies
var corsOptions = {
  origin: '*',
  optionsSuccessStatus: 200,
}
app.use(cors(corsOptions));




// Routes
app.use('/api/', imageRoutes); // Use image router

// Create HTTP server
const server = http.createServer(app);




const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"],
  },
});

let socket ;

io.on("connection", (clientSocket) => {
  socket = clientSocket
  console.log(`User Connected: ${socket.id}`);
  
  // When a user connects, store the socket reference with the user ID
  socket.on("set_user_id", (userId) => {
    connectedUsers[userId] = socket;
  });

  socket.on("join_room", (data) => {
    socket.join(data);
  });

  socket.on("send_message", (data) => {
    socket.to(data.room).emit("receive_message", data);
  });

  socket.on("disconnect", () => {
        console.log(`User Disconnected: ${socket.id}`);
  });
});

// Function to send a message to the current connected socket
function sendMessageToCurrentSocket(message) {
  
  socket.emit("message", message);
}





// Root route
app.get('/', (req, res) => {
  sendMessageToCurrentSocket("hellow man from the server")
});

// Root route middleware for handling other routes
app.use((req, res, next) => {
    // This middleware will only be reached if no other routes match
    res.status(404).send('404 - Not Found');
});

// Start listening to the queue
listenToQueue();

// Start server
server.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
