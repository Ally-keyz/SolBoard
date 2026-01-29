import vlc
import time
import json
from websocket import WebSocketApp

instance = vlc.Instance("--fullscreen")
player = instance.media_player_new()

def play_video(url):
    print("▶ Playing:", url)
    media = instance.media_new(url)
    player.set_media(media)
    player.play()
    time.sleep(1)
    player.set_fullscreen(True)

def pause():
    player.pause()

def stop():
    player.stop()

def on_message(ws, message):
    data = json.loads(message)

    if data.get("url"):
        play_video(data["url"])

    if data.get("action") == "pause":
        pause()
    elif data.get("action") == "play":
        player.play()
    elif data.get("action") == "stop":
        stop()

ws = WebSocketApp(
    "ws://YOUR_SERVER_IP:3000/socket.io/?EIO=4&transport=websocket",
    on_message=on_message
)

ws.run_forever()
