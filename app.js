import express from "express";
import http from "http";
import mongoose from "mongoose";
import { Server } from "socket.io";
import multer from "multer";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import VideoModel from "./models/videoSchema.js";
/*  ESM dirname fix */
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);

const io = new Server(server, {
  cors: { origin: "*" }
});

app.use(cors());
app.use(express.json());
app.use("/videos", express.static(path.join(__dirname, "uploads")));

/* 🔗 MongoDB */
await mongoose.connect("mongodb+srv://manzialpe:gloire@cluster0.beqtnkj.mongodb.net/?appName=Cluster0");
console.log("✅ MongoDB connected");

/* 📤 Multer storage */
const storage = multer.diskStorage({
  destination: path.join(__dirname, "uploads"),
  filename: (_, file, cb) => {
    cb(null, Date.now() + "-" + file.originalname);
  }
});

const upload = multer({ storage });

/* 📤 Upload video */
app.post("/api/upload", upload.single("video"), async (req, res) => {
  const video = await VideoModel.create({
    title: req.file.originalname,
    filename: req.file.filename,
    url: `http://YOUR_SERVER_IP:3000/videos/${req.file.filename}`
  });

  res.json(video);
});

/* 📃 Get videos */
app.get("/api/videos", async (_, res) => {
  const videos = await VideoModel.find().sort({ createdAt: -1 });
  res.json(videos);
});

/* 📺 CAST VIDEO */
app.post("/api/cast/:id", async (req, res) => {
  const video = await VideoModel.findById(req.params.id);
  if (!video) return res.status(404).json({ error: "Video not found" });

  io.emit("cast-video", {
    url: video.url,
    title: video.title
  });

  res.json({ success: true });
});

/* 🎮 Playback controls */
io.on("connection", socket => {
  console.log("🟢 Connected:", socket.id);

  socket.on("control", data => {
    io.emit("control", data);
  });

  socket.on("disconnect", () => {
    console.log("🔴 Disconnected:", socket.id);
  });
});

server.listen(3000, () => {
  console.log("🚀 Server running on port 3000");
});
