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
chunk_size = 128

#sd.play(y, sample_rate)
#sd.wait()

#sample_rate, old_data = wavfile.read("blah-blah-blah.wav")
inFile = wave.open("blah-blah-blah.wav", "rb")
shrink_size = 1
sample_rate = int(inFile.getframerate()/shrink_size)

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(inFile.getsampwidth()), channels=1, rate=sample_rate, output=True)

data = inFile.readframes(inFile.getnframes())
data_arr = np.fromstring(data, dtype='int16')
data_arr = (data_arr.reshape((inFile.getnframes(), 2))).astype("int16")
data_arr = data_arr[:,0][::shrink_size]
print(data_arr.shape)

stream.write(data_arr.tostring())

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
        chunk = env.chunk_at_loc(self.loc, self)
        out_str = chunk.tostring()
        stream.write(out_str)
    

env.add_avatar("jeff", (0,0))
env.add_avatar("bob", (0,1))


for i in range(len(data_arr))[::chunk_size]:
    #print(i)
    env.avatars["jeff"].sound.add_chunk(data_arr[i:i+chunk_size])
    env.avatars["bob"].play_current_chunk()
# stop stream (4)
stream.stop_stream()
stream.close()

inFile.close()
# close PyAudio (5)
p.terminate()

"""
Problems:
1. Weird interference noises 
2. Is slowed down by a factor of 4 when fed through program


"""