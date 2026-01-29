import socketio
import vlc
import time
import ssl
import certifi
import urllib.request

# ----------------------------
# CONFIG
# ----------------------------
SERVER_URL = "https://solboard-1.onrender.com:3000"  # Make sure this is your server URL + port

# ----------------------------
# SOCKET.IO CLIENT SETUP
# ----------------------------
sio = socketio.Client(reconnection=True, ssl_verify=True)

# ----------------------------
# VLC PLAYER SETUP
# ----------------------------
# Enable hardware acceleration (mmal) on Raspberry Pi
instance = vlc.Instance("--fullscreen", "--avcodec-hw=mmal")
player = instance.media_player_new()


def play_video(url):
    """Play a video via VLC with fullscreen and proper state checking."""
    print(f"▶ Playing video: {url}")

    # Test if URL is reachable
    try:
        urllib.request.urlopen(url)
    except Exception as e:
        print(f"❌ Cannot reach video URL: {e}")
        return

    media = instance.media_new(url)
    player.set_media(media)
    player.play()

    # Wait until VLC is actually playing
    attempts = 0
    while player.get_state() != vlc.State.Playing and attempts < 50:
        time.sleep(0.1)
        attempts += 1

    if player.get_state() == vlc.State.Playing:
        player.set_fullscreen(True)
        print("✅ Video is playing in fullscreen")
    else:
        print("❌ VLC failed to start video")


# ----------------------------
# SOCKET.IO EVENTS
# ----------------------------
@sio.event
def connect():
    print("🟢 Connected to server")


@sio.event
def disconnect():
    print("🔴 Disconnected from server")


@sio.on("cast-video")
def on_cast(data):
    url = data.get("url")
    if url:
        play_video(url)
    else:
        print("❌ No URL received in cast-video event")


@sio.on("control")
def on_control(data):
    action = data.get("action")
    if not action:
        return

    if action == "pause":
        player.pause()
        print("⏸ Paused video")
    elif action == "play":
        player.play()
        print("▶ Resumed video")
    elif action == "stop":
        player.stop()
        print("⏹ Stopped video")
    else:
        print(f"❌ Unknown control action: {action}")


# ----------------------------
# CONNECT TO SERVER
# ----------------------------
try:
    print(f"🌐 Connecting to server at {SERVER_URL} ...")
    sio.connect(SERVER_URL)
    sio.wait()
except Exception as e:
    print(f"❌ Failed to connect to server: {e}")
