import vlc
import RPi.GPIO as GPIO
from time import sleep
import os

video_dir = "/media/medialab/ROBERT"

haveDrive = False
for x in range(5):
    if os.path.exists(video_dir):
        haveDrive = True
        break
    sleep(30)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

_VIDEO_EXTS = ('.mp4', '.m4v', '.mov', '.avi', '.mkv')

video_list = [os.path.join(video_dir, f)
for f in sorted(os.listdir(video_dir))
if os.path.splitext(f)[1] in _VIDEO_EXTS]

current_index = -1
player = vlc.Instance()
media_player = vlc.MediaListPlayer()
mplayer = player.media_player_new()
mplayer.toggle_fullscreen()
media_player.set_media_player(mplayer)
media_list = player.media_list_new()

for v in video_list:
    media = player.media_new(v)
    media_list.add_media(media)
    
media_player.set_media_list(media_list)

print("Waiting for button input...")

while True:
    if GPIO.input(7) == GPIO.HIGH:
        print("Pin 7 is HIGH")
        mplayer.toggle_fullscreen()
    if GPIO.input(11) == GPIO.HIGH:
        print("Pin 11 is HIGH")
        if current_index == 1:
            if media_player.is_playing() == 0:
                if media_player.get_state() == 4:
                    media_player.play()
                if media_player.get_state() == 5 or media_player.get_state() == 6 or media_player.get_state() == 7:
                    media_player.play_item_at_index(0)
            else: 
                media_player.pause()
        else:
            media_player.play_item_at_index(0)
        current_index = 1
    if GPIO.input(13) == GPIO.HIGH:
        print("Pin 13 is HIGH")
        if current_index == 2:
            if media_player.is_playing() == 0:
                if media_player.get_state() == 4:
                    media_player.play()
                if media_player.get_state() == 5 or media_player.get_state() == 6 or media_player.get_state() == 7:
                    media_player.play_item_at_index(1)
            else: 
                media_player.pause()
        else:
            media_player.play_item_at_index(1)
        current_index = 2
    if GPIO.input(15) == GPIO.HIGH:
        print("Pin 15 is HIGH")
        if current_index == 3:
            if media_player.is_playing() == 0:
                if media_player.get_state() == 4:
                    media_player.play()
                if media_player.get_state() == 5 or media_player.get_state() == 6 or media_player.get_state() == 7:
                    media_player.play_item_at_index(2)
            else: 
                media_player.pause()
        else:
            media_player.play_item_at_index(2)
        current_index = 3
    if GPIO.input(16) == GPIO.HIGH:
        print("Pin 16 is HIGH")
        if current_index == 4:
            if media_player.is_playing() == 0:
                if media_player.get_state() == 4:
                    media_player.play()
                if media_player.get_state() == 5 or media_player.get_state() == 6 or media_player.get_state() == 7:
                    media_player.play_item_at_index(3)
            else: 
                media_player.pause()
        else:
            media_player.play_item_at_index(3)
        current_index = 4
    sleep(0.15)
print("Program is complete...")