from lib.DM858E import DM858E
from lib.IT6322A import IT6322A
import time
import os
import numpy as np

resource1_name ='USB0::0x1AB1::0x210B::DM8E260300157::INSTR'
resource2_name = 'USB0::0xFFFF::0x6300::602071010727630007::INSTR'
multimeter = DM858E(resource1_name)
power_supply = IT6322A(resource2_name)
data = []
power_supply.output_on()

for voltage in range(0, 7, 1):
    power_supply.set_voltage('CH2', voltage)
    time.sleep(1)
    data.append(multimeter.measure('voltage','dc'))
    time.sleep(1)

data_dir = '/Users/yangchen/Desktop/Devices-Control/Data'
file_path = os.path.join(data_dir, 'experiment1.csv')
np.savetxt(file_path, data, delimiter=",")

    