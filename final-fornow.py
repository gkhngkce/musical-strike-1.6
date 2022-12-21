#The source that we used to get information about notes, midi numbers, frequencies, and formulas reffrence
#https://newt.phys.unsw.edu.au/jw/notes.html

import numpy as np
import pyaudio
import pydirectinput
import pyautogui

#control's configuration variables
SPEED = 1 #set to preference
isWToggled=False
isEToggled=False

#note detection configuration variables
NOTE_MIN = 72       # C4 // guitar 40
NOTE_MAX = 85       # A4 // guitar 64
FSAMP = 48000       # Sampling frequency in Hzw original was 22050
FRAME_SIZE = 1024   # How many samples per frame? default was 2048
FRAMES_PER_FFT = 8  # FFT takes average across how many frames? default was 16

SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

# For printing out notes
NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()  # DGBE

#Calculations for notes w
def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1)

def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP

def mapping(midiNumber):
    if midiNumber == 81:#down
        pyautogui.moveRel(0, SPEED,_pause=False)
    if midiNumber == 79:#up
        pyautogui.moveRel(0, -SPEED,_pause=False)
    if midiNumber == 83:#right
        pyautogui.moveRel(SPEED, 0,_pause=False)
    if midiNumber == 72:#left
        pyautogui.moveRel(-SPEED, 0,_pause=False)
    if midiNumber == 84:#click
        pyautogui.click()
    if midiNumber == 74:#right-click
        pyautogui.click(button="right")
    if midiNumber == 77: # experimental
        isWToggled=not isWToggled
        if(isWToggled):
            pydirectinput.keyDown('w')
        else:
            pydirectinput.keyUp('w')

imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

# Allocate space to run an FFT.
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

# Initialize audio stream
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                input_device_index=0,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()

# Create Hanning window function
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

# Print initial configuration check
print('sampling at {} Hz with max resolution of {} Hz'.format(FSAMP,FREQ_STEP))

# As long as we are getting data:
while stream.is_active():
    #Get stream to the buffer
    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)
    
    #get maximum frame for volume detection for treshold
    vol=max(buf[-FRAME_SIZE:])
    #print(vol)
    if vol>=200:
        # Run the FFT on the windowed buffer
        fft = np.fft.rfft(buf * window)

        # Get frequency of maximum response in range
        freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

        # Get note number and nearest note
        n = freq_to_number(freq)
        n0 = int(round(n))
        
        # Console output once we have a full buffer
        num_frames += 1

        if num_frames >= FRAMES_PER_FFT:
            print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}  number:{}'.format(freq, note_name(n0), n-n0,n0))
            #mapping(n0)
            if n0 == 81:#down
                pyautogui.moveRel(0, SPEED,_pause=False)
            if n0 == 79:#up
                pyautogui.moveRel(0, -SPEED,_pause=False)
            if n0 == 83:#right
                pyautogui.moveRel(SPEED, 0,_pause=False)
            if n0 == 72:#left
                pyautogui.moveRel(-SPEED, 0,_pause=False)
            if n0 == 84:#click
                pyautogui.click()
            if n0 == 74:#right-click
                pyautogui.click(button="right")
            if n0 == 77: # experimental
                isWToggled=not isWToggled
                if(isWToggled):
                    pydirectinput.keyDown('w')
                else:
                    pydirectinput.keyUp('w')