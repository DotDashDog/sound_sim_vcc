import numpy as np
import math
import matplotlib.pyplot as plt
#import sounddevice as sd
#import time
#from scipy.io import wavfile
import wave
#import soundcard as sc
import pyaudio

sound_speed = 343
chunk_size = 32
mic_channels = 1
speaker_channels = 2
str_format = pyaudio.paInt16
record_secs = 20
shrink_size = 2

#sd.play(y, sample_rate)
#sd.wait()

#sample_rate, old_data = wavfile.read("blah-blah-blah.wav")
inFile = wave.open("blah-blah-blah.wav", "rb")
sample_rate = int(inFile.getframerate()/shrink_size)

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(inFile.getsampwidth()), channels=speaker_channels, rate=sample_rate, output=True)

file_data = inFile.readframes(inFile.getnframes())
data_arr = np.frombuffer(file_data, dtype='int16')
data_arr = (data_arr.reshape((inFile.getnframes(), 2))).astype("int16")
data_arr = data_arr[:,0][::shrink_size]

#stream.write(data_arr.tostring())

def start_mic_stream():
    global mic_stream
    mic_stream = p.open(format=str_format, channels=mic_channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
start_mic_stream()

def calc_dist(loc1, loc2):
    return math.sqrt((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2)


class Environment:
    def __init__(self):
        self.avatars = {}

    def add_avatar(self, name, loc):
        self.avatars[name] = Avatar(loc)

    def chunk_at_loc(self, loc, listener):
        total_chunk = np.zeros(chunk_size)
        for name in self.avatars:
            if self.avatars[name] != listener:
                try:
                    distance = calc_dist(loc, self.avatars[name].loc)
                    start_index = int(distance/sound_speed*sample_rate)
                    chunk = np.array(self.avatars[name].sound.past_vals[start_index:start_index+chunk_size])/(distance**2)
                    total_chunk = np.add(total_chunk, chunk)
                except IndexError:
                    print("INDEX ERROR")
                    placeholder
        return total_chunk


env = Environment()

numExceptions = 0

class Sound:
    def __init__(self, loc):
        self.storage_size = 2048
        self.past_vals = np.zeros(self.storage_size)
        self.loc = loc

    def add_chunk(self, chunk):
        self.past_vals = np.insert(self.past_vals, 0, chunk)
        if len(self.past_vals) > self.storage_size:
            self.past_vals = np.delete(self.past_vals, np.s_[len(self.past_vals)-chunk_size-1:len(self.past_vals)-1])


class Avatar:
    def __init__(self, loc):
        self.loc = loc
        self.sound = Sound(loc)

    def play_current_chunk(self):
        chunk = np.vstack((env.chunk_at_loc(self.loc, self), env.chunk_at_loc((self.loc[0], self.loc[1]-2), self))).astype("int16")
        out_str = chunk.tostring()
        stream.write(out_str)
    

env.add_avatar("talker1", (0, 3))
env.add_avatar("talker2", (0, -3))
env.add_avatar("listener", (0, 0))

"""
#Play from array
for i in range(len(data_arr))[::chunk_size]:
    #print(i)
    env.avatars["talker1"].sound.add_chunk(data_arr[i:i+chunk_size])
    try:
        data = np.fromstring(mic_stream.read(chunk_size), dtype='int16')
    except OSError:
        print("Exception")
        data = np.zeros(chunk_size)
        #mic_stream.stop_stream()
        #mic_stream.close()
        start_mic_stream()
        
    env.avatars["talker2"].sound.add_chunk(data)
    env.avatars["listener"].play_current_chunk()
"""

#Play from mic
#print("Starting")

for i in range(0, int(sample_rate / chunk_size * record_secs)):
    try:
        data = np.frombuffer(mic_stream.read(chunk_size), dtype='int16')
    except OSError:
        print("Exception")
        data = np.zeros(chunk_size)
        #mic_stream.stop_stream()
        #mic_stream.close()
        start_mic_stream()
        
    env.avatars["talker1"].sound.add_chunk(data)
    env.avatars["listener"].play_current_chunk()
print("Done")


# stop stream (4)
stream.stop_stream()
stream.close()
mic_stream.stop_stream()
mic_stream.close()

inFile.close()
# close PyAudio (5)
p.terminate()

"""
Problems:
1. Weird fuzziness if shrink_size is set to 1, likely because my computer can't run fast enough to add all amplitudes to stream in time.
2. Input Overflow Error in some cases for mic

"""