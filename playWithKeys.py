import playsound
import keyboard

#This is expermental place for testing purposes to play notes with keys without a flute

#This code is not completed ! So don't use it for now. Wait for next updates :)

while True: 
    if keyboard.is_pressed('8'):
        playsound.playsound('./flute-notes/1.mp3', True)
    if keyboard.is_pressed('2'):
        playsound.playsound('./flute-notes/2.mp3', True)
    if keyboard.is_pressed('4'):
        playsound.playsound('./flute-notes/3.mp3', True)
    if keyboard.is_pressed('6'):
        playsound.playsound('./flute-notes/4.mp3', True)
    if keyboard.is_pressed('7'):
        playsound.playsound('./flute-notes/0.mp3', True)
    if keyboard.is_pressed('9'):
        playsound.playsound('./flute-notes/5.mp3', True)
    if keyboard.is_pressed('1'):
        playsound.playsound('./flute-notes/6.mp3', True)
    if keyboard.is_pressed('3'):
        playsound.playsound('./flute-notes/7.mp3', True)