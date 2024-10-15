from lib.DG4062 import DG4062
from lib.OE1022 import OE1022
import time
import os
import numpy as np

resource_name1 = 'USB0::0x1AB1::0x0641::DG4E182101276::INSTR'
resource_name2 = '/dev/cu.usbserial-120'
generator = DG4062(resource_name1)
lock_in_amp = OE1022(resource_name2)
data = []
amp_list = []

#疑问1：reset()的默认设置到底是什么？它是否符合我们的测量要求？
#疑问2：set_harmonic()的第一个参数是什么意思——谐波通道
# lock_in_amp.set_harmonic(1,1)
# lock_in_amp.set_harmonic(2,2)
# lock_in_amp.set_buffer_selection(2, 'Rh2')


# 直接设置交变电压（mVpp）的幅值
for amp in range(2,83,2):
    amp_list.append(amp*0.001)

# 设置交变恒流源t提供1mA的交变电源
generator.apply_sine_wave(1, 3.14, 13e-3, 0, 0)
generator.set_output_state(1, 'ON')

n = 1
for i in range(1, 3):
    data.append(n*1000)
    n = n + 1

    for amp in amp_list:
        generator.apply_sine_wave(2, 3.14, amp , 0, 0)
        generator.set_output_state(2, 'ON')
        time.sleep(10)
        lock_in_amp.reset()
        lock_in_amp.set_harmonic(1,1)
        lock_in_amp.set_buffer_selection(1, 'Rh1')
        lock_in_amp.get_start()
        time.sleep(3)
        lock_in_amp.stop()
        value = lock_in_amp.read_buffer_data(1, 0, 50)
        # print(value)
        # print(value[1:len(value)-1])
        mean, variance, std_deviation = lock_in_amp.calculate_statistics(value[1:len(value)-1])
        # print('mean=',mean, 'variance=',variance, 'std_deviation=',std_deviation)
        print(f'Amplitude: {amp*1000} mVpp, Value: {mean*1000} mV')
        data.append(float(mean*1000))
    
    
    
data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, 'AC&AC实验 .csv')
np.savetxt(file_path, data, delimiter=",")
