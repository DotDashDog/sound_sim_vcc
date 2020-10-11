import numpy as np
import math
import matplotlib.pyplot as plt
import sounddevice as sd
import time
from scipy.io import wavfile
import soundcard as sc
import pyaudio

sound_speed = 343

#sd.play(y, sample_rate)
#sd.wait()

sample_rate, data = wavfile.read("blah-blah-blah.wav")
#sd.play(data, sample_rate)
#sd.wait()
new_data = data
batch_per_sec = 100
batch_size = int(sample_rate/batch_per_sec)
for i in range(batch_per_sec):
    sd.play(data[batch_size*i:batch_size*i+1], sample_rate)
sd.wait()

def calc_dist(loc1, loc2):
    return math.sqrt((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2)


class Environment:
    def __init__(self):
        self.avatars = np.array([])

    def add_avatar(self, avatar):
        np.append(self.avatars, avatar)

    def amp_at_loc(self, loc):
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
            return self.past_vals[distance/sound_speed*samplerate]/distance**2
        except:
            return 0


class Avatar:
    def __init__(self, loc):
        self.loc = loc
        self.sound = Sound(loc)

    def play_current_frame(self):
        amp = env.amp_at_loc(self.loc)