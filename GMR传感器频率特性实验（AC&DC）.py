from lib.DG4062 import DG4062
from lib.OE1022 import OE1022
from lib.DP2031 import DP2031
import time
import os
import numpy as np

resource_name1 = 'USB0::0x1AB1::0x0641::DG4E182101266::INSTR'
resource_name2 = '/dev/cu.usbserial-120'
resource_name3 = 'USB0::0x1AB1::0xA4A8::DP2A242800127::INSTR'

generator = DG4062(resource_name1)
lock_in_amp = OE1022(resource_name2)
power_supply = DP2031(resource_name3)
data = []
freq_list = [3.14,10,20,30,50,100,200,300,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000]

#设置励磁电流大小分别为3mA、5mA、10mA、20mA
current = 3
power_supply.set_voltage('CH3', 5)
power_supply.set_current('CH3', current*0.001)
power_supply.output_on()

# 改变AC恒流源的频率大小并进行测量
for freq in freq_list:
    generator.apply_sine_wave(1, freq , 14.4e-3 , 0, 0)
    generator.set_output_state(1, 'ON')
    time.sleep(15)
    lock_in_amp.reset()
    lock_in_amp.set_harmonic(1,1)
    lock_in_amp.set_buffer_selection(1, 'Rh1')
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 50)
    data.append(float(value[0]))
    print(f'Freq: {freq} Hz, Value: {float(value[0])}')

# 存储数据
data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, 'GMR传感器频率特性.csv')
np.savetxt(file_path, data, delimiter=",")