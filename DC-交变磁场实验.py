from lib.DG4202 import DG4202
from lib.OE1022 import OE1022
import time
import os
import numpy as np

resource_name = 'USB0::0x1AB1::0x0641::DG4E195204310::INSTR'
resource_name2 = 'USB0::0x1AB1::0x210B::DM8E260300157::INSTR'
lock_in_amp = OE1022(resource_name2)
generator = DG4202(resource_name)
data = []
amp_list = []

#疑问1：reset()的默认设置到底是什么？它是否符合我们的测量要求？
#疑问2：set_harmonic()的第一个参数是什么意思？
lock_in_amp.reset()
lock_in_amp.set_harmonic(1,1)
lock_in_amp.set_buffer_selection(1, 'Rh1')

for i in range(0, 41, 2):
    amp = 6.03148 * i - 0.13831
    amp_list.append(amp)

for amp in amp_list:
    generator.apply_sine_wave(1, 3.14, amp , 0, 0)
    generator.set_output_state(1, 'ON')
    time.sleep(5)
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 50)
    n = len(value)
    mean_value = sum(value) / n
    data.append(mean_value)
    
data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, 'DC_交变磁场实验.csv')
np.savetxt(file_path, data, delimiter=",")
