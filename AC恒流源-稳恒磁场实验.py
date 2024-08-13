# from lib.DG4062 import DG4062
from lib.OE1022 import OE1022
from lib.DP2031 import DP2031
import time
import os
import numpy as np

# resource_name = 'USB0::0x1AB1::0x0641::DG4E182101266::INSTR'
resource_name2 = '/dev/cu.usbserial-1120'
resource_name3 = 'USB0::0x1AB1::0xA4A8::DP2A242800127::INSTR'
power_supply = DP2031(resource_name3)
lock_in_amp = OE1022(resource_name2)
# generator = DG4062(resource_name)
data = []
amp_list = []

# 设置锁相放大器的参数
lock_in_amp.reset()
lock_in_amp.set_harmonic(1,1)

lock_in_amp.set_buffer_selection(1, 'Rh1')


# 设置交变恒流源提供1mA的交变电源
# amp = 14.4
# generator.apply_sine_wave(1, 3.14, amp , 0, 0)
# generator.set_output_state(1, 'ON')

# 调整DC励磁电流大小，并进行测量
for current in range(0,51,2):
    power_supply.set_voltage('CH3', 5)
    power_supply.set_current('CH3', current*0.001)
    power_supply.output_on()
    time.sleep(15)
    lock_in_amp.reset()
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 50)
    n = len(value)
    mean_value = sum(value) / n
    data.append(mean_value)
    print(f'Current: {current} mA, Mean Value: {mean_value}')
    

# 存储数据
data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, 'DC_交变磁场实验.csv')
np.savetxt(file_path, data, delimiter=",")