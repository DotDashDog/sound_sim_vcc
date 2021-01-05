import numpy as np
import math
import matplotlib.pyplot as plt
import wave
#import soundcard as sc
import pyaudio

def to_radians(degrees):
    return degrees*math.pi/180

def calc_dist(p1, p2):
    return math.sqrt((p1[0]+p2[0])**2+(p1[1]+p2[1])**2)

p = pyaudio.PyAudio()

inFile = wave.open("blah-blah-blah.wav", "rb")

samp_width = inFile.getsampwidth()
print("Sample Width: " + str(samp_width))
data_type = "int" + str(8*samp_width)

num_channels = inFile.getnchannels()
print("Channels: " + str(num_channels))

framerate = inFile.getframerate()
print("Framerate: " + str(framerate))

num_frames = inFile.getnframes()
print("Frames: " + str(num_frames))

file_length = num_frames/framerate
print("Seconds: " + str(file_length))

print("Format: " + str(p.get_format_from_width(samp_width)))

print("Data: " + str(p.get_default_host_api_info()))

print("Default Output Info: " + str(p.get_default_output_device_info()))

speaker_stream = p.open(format=p.get_format_from_width(samp_width), channels=num_channels, rate=framerate, output=True)


data = inFile.readframes(num_frames)

data_array = np.frombuffer(data, "int16")
data_array = np.reshape(data_array, (-1,2)).copy()
print(np.max(data_array))
print(data_array.shape)
data_array.setflags(write=1)

angle = 0
ear_dist = 0.15 #0.15
person_pos = (0, 0)
sound_pos = (3, 0)
ear_1_pos = (person_pos[0]+(math.cos(to_radians(angle))*(ear_dist/2)), person_pos[1]+(math.sin(to_radians(angle))*(ear_dist/2)))
ear_2_pos = (person_pos[0]-(math.cos(to_radians(angle))*(ear_dist/2)), person_pos[1]-(math.sin(to_radians(angle))*(ear_dist/2)))

print("Ear 1: " + str(ear_1_pos))
print("Ear 2: " + str(ear_2_pos))
print("Person: " + str(person_pos))

data_array = data_array.astype(float)
data_array[:,0] /= calc_dist(sound_pos, ear_1_pos)**2
data_array[:,1] /= calc_dist(sound_pos, ear_2_pos)**2
#data_array[:,0] = 0
data_array = data_array.astype("int16")

new_data = data_array.tobytes()

#data_array = np.frombuffer(new_data, "int16")
#data_array = np.reshape(data_array, (-1,2))
#print(np.max(data_array))
#print(data_array.shape)

speaker_stream.write(new_data)

print("Done")

speaker_stream.stop_stream()
speaker_stream.close()
p.terminate()