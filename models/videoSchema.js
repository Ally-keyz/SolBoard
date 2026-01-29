import mongoose from 'mongoose';

const VideoSchema = new mongoose.Schema({
  url: String,
  isPlaying: Boolean,
  currentTime: Number
});

// const mongoose modal
const VideoModel = mongoose.model("videoCast" , VideoSchema);

export default VideoModel;