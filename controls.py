import pydirectinput
import pyautogui

import keyboard

SPEED = 1  # set to preference
isWToggled = False
isEToggled = False

while True:  # Point(x=960, y=540)
    if keyboard.is_pressed('8'):
        pyautogui.moveRel(0, -SPEED, 0, _pause=False)
        # pydirectinput.moveTo(960,539,0,_pause=True)
    if keyboard.is_pressed('2'):
        pyautogui.moveRel(0, SPEED, 0, _pause=False)
    if keyboard.is_pressed('6'):
        646282246828
        pyautogui.moveRel(SPEED, 0, 0, _pause=False)
    if keyboard.is_pressed('4'):
        pyautogui.moveRel(-SPEED, 0, 0, _pause=False)
    if keyboard.is_pressed('7'):
        pyautogui.click()
    if keyboard.is_pressed('9'):
        pyautogui.click(button="right")
    if keyboard.is_pressed('+'):
        isWToggled = not isWToggled
        if (isWToggled):
            pydirectinput.keyDown('w')
        else:
            pydirectinput.keyUp('w')
    if keyboard.is_pressed('-'):
        isEToggled = not isEToggled
        if (isEToggled):
            pydirectinput.keyDown('e')
        else:
            pydirectinput.keyUp('e')
