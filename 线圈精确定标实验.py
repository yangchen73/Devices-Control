from lib.DG4062 import DG4062
from lib.OE1022 import OE1022
import time
import os
import numpy as np

resource_name1 = 'USB0::0x1AB1::0x0641::DG4E182101266::INSTR'
resource_name2 = '/dev/cu.usbserial-120'
generator = DG4062(resource_name1)
lock_in_amp = OE1022(resource_name2)
data = []
data2 = []
data3 = []

for amp in range(50, 1401, 50):
    a = amp / 1000
    generator.apply_sine_wave(1, 3.14, a , 0, 0)
    generator.set_output_state(1, 'ON')
    time.sleep(13)
    lock_in_amp.reset()
    lock_in_amp.set_harmonic(1,1)
    lock_in_amp.set_buffer_selection(1, 'Rh1')
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 11)
    data.append(float(value[0]))
    print(f'Amplitude: {amp} mVpp, Value: {value[0]}')
    print('-----------------------------------')
    print(value)

generator.set_output_state(1, 'OFF')


data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, '线圈精确定标实验1.csv')
np.savetxt(file_path, data, delimiter=",")

time.sleep(15)

for amp in range(50, 1401, 50):
    a = amp / 1000
    generator.apply_sine_wave(1, 3.14, a , 0, 0)
    generator.set_output_state(1, 'ON')
    time.sleep(13)
    lock_in_amp.reset()
    lock_in_amp.set_harmonic(1,1)
    lock_in_amp.set_buffer_selection(1, 'Rh1')
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 11)
    data2.append(float(value[0]))
    print(f'Amplitude: {amp} mVpp, Value: {value[0]}')
    print('-----------------------------------')
    print(value)

generator.set_output_state(1, 'OFF')


data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, '线圈精确定标实验2.csv')
np.savetxt(file_path, data2, delimiter=",")

time.sleep(15)

for amp in range(50, 1401, 50):
    a = amp / 1000
    generator.apply_sine_wave(1, 3.14, a , 0, 0)
    generator.set_output_state(1, 'ON')
    time.sleep(13)
    lock_in_amp.reset()
    lock_in_amp.set_harmonic(1,1)
    lock_in_amp.set_buffer_selection(1, 'Rh1')
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 11)
    data3.append(float(value[0]))
    print(f'Amplitude: {amp} mVpp, Value: {value[0]}')
    print('-----------------------------------')
    print(value)

generator.set_output_state(1, 'OFF')


data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, '线圈精确定标实验3.csv')
np.savetxt(file_path, data3, delimiter=",")