#The source that we used to get information about notes, midi numbers, frequencies, and formulas reffrence
#https://newt.phys.unsw.edu.au/jw/notes.html

#note midinumber maps

#84-85-86 midi 0 'Left Click'
#82-83 0,1 'up'
#81 0,1,2 'down'
#79,80 0,1,2,3 'left'
#77-78 0,1,2,3,4 'right'
#76 0,1,2,3,4,5 (bazen kayıyıyor) 'Right Click'
#74 0,1,2,3,4,5,6 'E'
#72 0,1,2,3,4,5,6,7 'W'

import numpy as np
import pyaudio
import pydirectinput
import pyautogui
import time


#control's configuration variablese
SPEED = 1 #set to preference
SPEED_MODIFIER=30 #how much accelerate will it gain
DEVICE_INDEX=1 #input device index(You can get desired device from find-input-device-index.py)
MAX_ACCELERATION=3 #Do not increase more than 3 for prevent skipping

#global variables for toggle 'e' and 'w'
isWToggled = False 
isEToggled = False

#For measure response time
starttime=0
endtime=0

#note detection configuration variables
NOTE_MIN = 72       # C4 // change it with respect to note-reffrence.jpg according to desired instrument
NOTE_MAX = 85       # A4 // change it with respect to note-reffrence.jpg according to desired instrument
FSAMP = 48000       # Sampling frequency in Hz // default was 22050
FRAME_SIZE = 1024   # How many samples per frame? // default was 2048
FRAMES_PER_FFT = 8  # FFT takes average across how many frames?  // default was 16

SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

# For printing out notes
NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()  # DGBE
NOTE_COUNTS=np.zeros(90) #The list that we keep track of note occurance

#Calculations for notes
def freq_to_number(f): return 69 + 12*np.log2(f/440.0)

def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)

def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1)

def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP

#The function that keeps the track of occurances
def noteCounter(midi):
    global NOTE_COUNTS
    if(NOTE_COUNTS[midi]>=1):
        NOTE_COUNTS[midi]+=1
    elif(NOTE_COUNTS[midi]<1):
        
        NOTE_COUNTS=np.zeros(90)
        NOTE_COUNTS[midi]+=1
    #print("midi {} count {}".format(midi,NOTE_COUNTS[midi]))

#While playing get some acceleration on the speed
def calculateSpeedModifier(midi):
    return min(MAX_ACCELERATION,(SPEED+(NOTE_COUNTS[midi]/SPEED_MODIFIER)+(NOTE_COUNTS[midi]/SPEED_MODIFIER)))

#Key toggler
def toggleKey(key,keyState):
    if(keyState):
        pydirectinput.keyDown(key)
    else:
        pydirectinput.keyUp(key)
    return not keyState

#Mapping midi numbers to keys, clicks, movement
def mapping(midiNumber):
    if midiNumber == 82 or midiNumber == 83:#up
        pyautogui.moveRel(0, -calculateSpeedModifier(midiNumber),_pause=False)
    elif midiNumber == 81:#down
        pyautogui.moveRel(0, calculateSpeedModifier(midiNumber),_pause=False)
    elif midiNumber == 79 or midiNumber == 80:#left
        pyautogui.moveRel(-calculateSpeedModifier(midiNumber), 0,_pause=False)    
    elif midiNumber == 77 or midiNumber == 78:#right
        pyautogui.moveRel(calculateSpeedModifier(midiNumber), 0,_pause=False)
    elif (midiNumber==84 and NOTE_COUNTS[84]<=1) or (midiNumber==85 and NOTE_COUNTS[85]<=1) or (midiNumber==86 and NOTE_COUNTS[86]<=1):#click
        pyautogui.click()
    elif midiNumber == 76 and NOTE_COUNTS[76]<=1:#right-click
        pyautogui.click(button="right")
    elif midiNumber == 72 and NOTE_COUNTS[72]<=1: # experimental
        global isWToggled
        isWToggled = toggleKey('w',isWToggled)
    elif midiNumber == 74 and NOTE_COUNTS[74]<=1: # experimental
        global isEToggled
        isWToggled = toggleKey('e',isWToggled)


#Range for note detection with FFT
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
                                input_device_index=DEVICE_INDEX,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()

# Create Hanning window function(filter)
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

# Print initial configuration check
print('Sampling at {} Hz with resolution of {} Hz'.format(FSAMP,FREQ_STEP))
p=pyaudio.PyAudio()
print("Getting stream from {}".format(p.get_device_info_by_index(DEVICE_INDEX).get("name")))

# As long as we are getting data:
while stream.is_active():
    starttime=time.time()
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
            #print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}  number:{} occurance:{}'.format(freq, note_name(n0), n-n0,n0,NOTE_COUNTS[n0]))
            noteCounter(n0)
            mapping(n0)
            endtime=time.time()
            print("Exectime: ",endtime-starttime)
    else:
        noteCounter(0)
        #print("Acceleration lost")