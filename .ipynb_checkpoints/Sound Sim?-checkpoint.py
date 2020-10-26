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
chunk_size = 100

#sd.play(y, sample_rate)
#sd.wait()

#sample_rate, old_data = wavfile.read("blah-blah-blah.wav")
inFile = wave.open("blah-blah-blah.wav", "rb")
sample_rate = inFile.getframerate()
# instantiate PyAudio (1)
p = pyaudio.PyAudio()
# open stream (2)
stream = p.open(format=p.get_format_from_width(inFile.getsampwidth()), channels=inFile.getnchannels(), rate=inFile.getframerate(), output=True)

data = inFile.readframes(inFile.getnframes())
data_arr = np.fromstring(data, dtype='int16')
data_arr = (data_arr.reshape((inFile.getnframes(), 2))).astype("int16")
# play stream (3)
a = np.array([0, 1, 2, 3, 4, 5])
for i in range(0,10):
    a = np.insert(a, 1, 0)
    a = np.delete(a, 5)
    print(a)
    print(len(a))

#stream.write(data)

"""for i in range(0, len(data)-1, chunk_size):
    chunk = data[i:i+chunk_size]
    stream.write(chunk)"""


def calc_dist(loc1, loc2):
    return math.sqrt((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2)


class Environment:
    def __init__(self):
        self.avatars = {}

    def add_avatar(self, name, loc):
        self.avatars[name] = Avatar(loc)

    def chunk_at_loc(self, loc, listener):
        total_amp = 0
        for name in self.avatars:
            if self.avatars[name] != listener:
                total_amp += self.avatars[name].sound.hear_amp(calc_dist(loc, self.avatars[name].loc))
        return total_amp


env = Environment()

numExceptions = 0

class Sound:
    def __init__(self, loc):
        self.past_vals = []
        self.loc = loc

    def add_amp(self, amp):
        self.past_vals.insert(0, amp)
        if len(self.past_vals) > 10000:
            #print(len(self.past_vals))
            self.past_vals.pop(len(self.past_vals)-1)
            #print(len(self.past_vals))

    def hear_amp(self, distance):
        try:
            #print(int(distance/sound_speed*sample_rate))
            return self.past_vals[int(distance/sound_speed*sample_rate)]/(distance**2)
        except IndexError:
            #global numExceptions 
            #numExceptions += 1
            return 0


class Avatar:
    def __init__(self, loc):
        self.loc = loc
        self.sound = Sound(loc)

    def play_current_chunk(self):
        batch = env.chunk_at_loc(self.loc, self)
        out_str = np.array(frame).tostring()
        stream.write(out_str)
    

env.add_avatar("jeff", (0,0))
env.add_avatar("bob", (0,1))

#print(env.avatars)

for i in data_arr:
    env.avatars["jeff"].sound.add_amp(i)
    env.avatars["bob"].play_current_frame()

print(numExceptions)
# stop stream (4)
stream.stop_stream()
stream.close()

inFile.close()
# close PyAudio (5)
p.terminate()