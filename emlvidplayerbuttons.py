import vlc
import RPi.GPIO as GPIO
from time import sleep
import os

# Change these variables to match the paths and GPIO pins used in the Boxplay 

video_dir = "/media/medialab/ROBERT/" #PATH to the videos
application_dir = "/home/medialab/pyprojects/emlvidplayerbuttons/" #PATH to the application
gpio_reboot_pin = 7 #RPI GPIO Pin used to reboot the system
video_1_pin = 13 #RPI GPIO Pin used to play Video 1
video_2_pin = 11 #RPI GPIO Pin used to play Video 2
video_3_pin = 15 #RPI GPIO Pin used to play Video 3
video_4_pin = 16 #RPI GPIO Pin used to play Video 4
video_exts = ('.mp4', '.m4v', '.mov', '.avi', '.mkv') #Extensions the app will see as valid in the video path

#
# There is no code below here that needs to be changed 
#

# This code delays the Boxplay code from running until the USB
# drive has mounted
haveDrive = False
for x in range(5):
    if os.path.exists(video_dir):
        haveDrive = True
        break
    sleep(30)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpio_reboot_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(video_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(video_2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(video_3_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(video_4_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

video_list = [os.path.join(video_dir, f)
for f in sorted(os.listdir(video_dir))
if os.path.splitext(f)[1] in video_exts]

current_index = -1
player = vlc.Instance()
media_player = vlc.MediaListPlayer()
mplayer = player.media_player_new()
mplayer.set_fullscreen(True)
media_player.set_media_player(mplayer)
media_list = player.media_list_new()

for v in video_list:
    media = player.media_new(v)
    media_list.add_media(media)

media = player.media_new(application_dir + "/emlboxplay_ready_loop.mp4")
media_list.add_media(media)

media_player.set_media_list(media_list)

# Play the black boxplay ready loop
media_player.play_item_at_index(4)
print("Waiting for button input...")

while True:
    # If both the 3 & 4 are pressed reboot the system
    if GPIO.input(video_3_pin) == GPIO.HIGH and GPIO.input(video_4_pin) == GPIO.HIGH:
        print("Reboot button sequence has been pressed")
        os.system("reboot")

    # If both the 1 & 2 are pressed together return to desktop
    if GPIO.input(video_1_pin) == GPIO.HIGH and GPIO.input(video_2_pin) == GPIO.HIGH:
        print("Exit fullscreen button sequnce has been pressed")
        mplayer.set_fullscreen(False)
    
    # If yellow button is pressed launch 1st video
    if GPIO.input(video_1_pin) == GPIO.HIGH:
        print("Video Button 1 has been pressed")
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
    
    # If top black button is pressed launch 2nd video
    if GPIO.input(video_2_pin) == GPIO.HIGH:
        print("Video Button 2 has been pressed")
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
    
    #If white button is pressed launch 3rd video
    if GPIO.input(video_3_pin) == GPIO.HIGH:
        print("Video 3 has been pressed")
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
    
    # If blue button is pressed launch 4th video
    if GPIO.input(video_4_pin) == GPIO.HIGH:
        print("Video 4 has been pressed")
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