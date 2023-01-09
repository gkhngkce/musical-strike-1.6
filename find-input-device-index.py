import pyaudio

p = pyaudio.PyAudio()

print("Devices ...")
for i in range(p.get_device_count()):
    print("Name: {} - Index: {}".format(p.get_device_info_by_index(i).get("name"),p.get_device_info_by_index(i).get("index")))