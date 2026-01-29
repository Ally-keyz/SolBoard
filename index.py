import socketio
import vlc
import time

sio = socketio.Client()

instance = vlc.Instance(
    "--fullscreen",
    "--avcodec-hw=mmal"
)
player = instance.media_player_new()

def play_video(url):
    print("▶ Playing:", url)
    media = instance.media_new(url)
    player.set_media(media)
    player.play()
    time.sleep(1)
    player.set_fullscreen(True)

@sio.event
def connect():
    print("🟢 Connected to server")

@sio.on("cast-video")
def on_cast(data):
    play_video(data["url"])

@sio.on("control")
def on_control(data):
    if data["action"] == "pause":
        player.pause()
    elif data["action"] == "play":
        player.play()
    elif data["action"] == "stop":
        player.stop()

sio.connect("https://solboard-1.onrender.com")
sio.wait()
