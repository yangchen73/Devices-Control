from lib.DG4062 import DG4062
from lib.OE1022 import OE1022
import time
import os
import numpy as np

resource_name1 = 'USB0::0x1AB1::0x0641::DG4E182101276::INSTR'
resource_name2 = '/dev/cu.usbserial-110'
generator = DG4062(resource_name1)
lock_in_amp = OE1022(resource_name2)
data = []
data2 = []
amp_list = []

# lock_in_amp.set_harmonic(1,1)
# lock_in_amp.set_harmonic(2,2)


# 直接设置励磁交变电压（mVpp）的幅值
for amp in range(2, 83, 2):
    amp_list.append(amp)


for amp in amp_list:
    generator.apply_sine_wave(1, 3.14, amp*0.001 , 0, 0)
    generator.set_output_state(1, 'ON')
    time.sleep(10)
    lock_in_amp.reset()
    lock_in_amp.set_harmonic(1,1)
    lock_in_amp.set_buffer_selection(1, 'Rh1')
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 50)
    # print(value)
    data.append(float(value[0]))
    print(f'Amplitude: {amp} mVpp, Value: {value[0]}')

generator.set_output_state(1, 'OFF')
generator.set_output_state(2, 'OFF')
    
data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, 'DC_交变磁场实验9-24.csv')
np.savetxt(file_path, data, delimiter=",")
