from lib.DM858E import DM858E
from lib.DP2031 import DP2031
import time
import os
import numpy as np


resource1_name ='USB0::0x1AB1::0x210B::DM8E260300157::INSTR'
resource2_name = 'USB0::0x1AB1::0xA4A8::DP2A242800127::INSTR'
multimeter = DM858E(resource1_name)
power_supply = DP2031(resource2_name)
data = []

# power_supply.set_voltage('CH1', 15)
# power_supply.set_current('CH1', 0.1)
# power_supply.output_on()
# power_supply.set_voltage('CH2', 7)
# power_supply.set_current('CH2', 0.1)
# power_supply.output_on()

# power_supply.set_voltage('CH1', 6)
# power_supply.set_current('CH1', 0.001)
# power_supply.output_on()
# time.sleep(10)
for current in range(0,101,5):
    power_supply.set_voltage('CH3', 5)
    power_supply.set_current('CH3', current*0.001)
    power_supply.output_on()
    time.sleep(3)
    data.append(1000*multimeter.measure('voltage','dc'))
    #默认单位是（V、A、Ω、Hz、s、%），量程是自动调节的
    # time.sleep(1)

power_supply.output_off('CH2')
power_supply.output_off('CH1')
power_supply.output_off('CH3')
data_dir = '/Users/a1-6/VScode/Physic Experiment Game/Devices-Control/Data'
file_path = os.path.join(data_dir, '6+6_calibration experiment.csv')
np.savetxt(file_path, data, delimiter=",")