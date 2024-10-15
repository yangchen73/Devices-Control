from lib.DG4062 import DG4062
from lib.OE1022 import OE1022
from lib.DP2031 import DP2031
import time
import os
import numpy as np

resource_name1 = 'USB0::0x1AB1::0x0641::DG4E182101276::INSTR'
resource_name2 = '/dev/cu.usbserial-120'
resource_name3 = 'USB0::0x1AB1::0xA4A8::DP2A242800127::INSTR'

generator = DG4062(resource_name1)
lock_in_amp = OE1022(resource_name2)
# power_supply = DP2031(resource_name3)
data = []
amp_list = []
data2 = []


# # 设置交变恒流源提供1mA的交变电源
generator.apply_sine_wave(1, 3.14, 13e-3 , 0, 0)
generator.set_output_state(1, 'ON')

# 调整DC励磁电流大小，并进行测量
for current in range(1,41,1):
    # power_supply.set_voltage('CH1', 5)
    # power_supply.set_current('CH1', current*0.0001)
    # power_supply.output_on()
    time.sleep(15)
    # 设置锁相放大器的参数
    lock_in_amp.reset()
    lock_in_amp.set_harmonic(1,1)
    lock_in_amp.set_buffer_selection(1, 'Rh1')
    lock_in_amp.get_start()
    time.sleep(3)
    lock_in_amp.stop()
    value = lock_in_amp.read_buffer_data(1, 0, 50)
    mean, variance, std_deviation = lock_in_amp.calculate_statistics(value[1:len(value)-1])
    print(f'Current: {current*0.1} mA, Value: {mean*1000} mV')
    data.append(float(mean*1000))

# generator.set_output_state(1, 'OFF')

# 存储数据
data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, 'AC&DC实验10-15.csv')
np.savetxt(file_path, data, delimiter=",")

# data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
# file_path = os.path.join(data_dir, 'AC_交变磁场实验2.csv')
# np.savetxt(file_path, data2, delimiter=",")