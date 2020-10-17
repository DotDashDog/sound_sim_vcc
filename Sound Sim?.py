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
chunk_size = 1024

#sd.play(y, sample_rate)
#sd.wait()

#sample_rate, old_data = wavfile.read("blah-blah-blah.wav")
inFile = wave.open("blah-blah-blah.wav", "rb")

# instantiate PyAudio (1)
p = pyaudio.PyAudio()
# open stream (2)
stream = p.open(format=p.get_format_from_width(inFile.getsampwidth()), channels=inFile.getnchannels(), rate=inFile.getframerate(), output=True)

data = inFile.readframes(inFile.getnframes())
data_arr = np.fromstring(data, dtype='int16')
data_arr = (data_arr.reshape((inFile.getnframes(), 2))*3).astype("int16")
data = data_arr.tostring()
# play stream (3)

stream.write(data)

"""for i in range(0, len(data)-1, chunk_size):
    chunk = data[i:i+chunk_size]
    stream.write(chunk)"""

# stop stream (4)
stream.stop_stream()
stream.close()

inFile.close()
# close PyAudio (5)
p.terminate()

def calc_dist(loc1, loc2):
    return math.sqrt((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2)


class Environment:
    def __init__(self):
        self.avatars = np.array([])

    def add_avatar(self, avatar):
        np.append(self.avatars, avatar)

    def amp_at_loc(self, loc, listener):
        total_amp = 0
        for avatar in self.avatars:
            total_amp += avatar.sound.hear_amp(calc_dist(loc, avatar.loc))
        return total_amp


env = Environment()


class Sound:
    def __init__(self, loc):
        self.past_vals = np.array([])
        self.loc = loc

    def add_amp(self, amp):
        np.insert(self.past_vals, 0, amp)

    def hear_amp(self, distance):
        try:
            return self.past_vals[distance/sound_speed*sample_rate]/distance**2
        except:
            return 0


class Avatar:
    def __init__(self, loc):
        self.loc = loc
        self.sound = Sound(loc)

    def play_current_frame(self):
        amp = env.amp_at_loc(self.loc, self)