from lib.DG4062 import DG4062
from lib.OE1022 import OE1022
import time
import os
import numpy as np

resource_name1 = 'USB0::0x1AB1::0x0641::DG4E182101266::INSTR'
resource_name2 = '/dev/cu.usbserial-1120'
generator = DG4062(resource_name1)
lock_in_amp = OE1022(resource_name2)
data = []
amp_list = []

#疑问1：reset()的默认设置到底是什么？它是否符合我们的测量要求？
#疑问2：set_harmonic()的第一个参数是什么意思？
lock_in_amp.set_harmonic(1,1)
lock_in_amp.set_harmonic(2,2)
# lock_in_amp.set_buffer_selection(2, 'Rh2')

# # 设置交变电流的幅值和步长，并转化为对应的交变电压的幅值
# for i in range(0, 41, 2):
#     amp = 6.03148 * i - 0.13831
#     amp_list.append(amp)

# 直接设置交变电压（mVpp）的幅值
for amp in range(10,401,20):

    amp_list.append(amp*0.001)

#设置交变恒流源t提供1mA的交变电源
# generator.apply_sine_wave(1, 3.14, 14.4e-3, 0, 0)
# generator.set_output_state(1, 'ON')

for amp in amp_list:
    generator.apply_sine_wave(2, 3.14, amp , 0, 0)
    generator.set_output_state(2, 'ON')
    time.sleep(15)
    lock_in_amp.reset()
    lock_in_amp.set_harmonic(1,1)
    lock_in_amp.set_harmonic(1,2)
    lock_in_amp.set_buffer_selection(1, 'Rh1')
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 50)
    # print(value)
    data.append(value[0])
    
    print(f'Amplitude: {amp} mVpp, Value: {value[0]}')
    
data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, 'DC_交变磁场实验.csv')
np.savetxt(file_path, data, delimiter=",")
