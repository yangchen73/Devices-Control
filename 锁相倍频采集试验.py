import time
from lib.OE1022 import OE1022

lock_in_amp = OE1022('/dev/cu.usbserial-120')  
lock_in_amp.reset()
lock_in_amp.set_harmonic(1,1)
lock_in_amp.set_harmonic(2,2)
lock_in_amp.set_buffer_selection(1, 'Rh1')
lock_in_amp.set_buffer_selection(2, 'Rh2') 
lock_in_amp.get_start()
time.sleep(3)
lock_in_amp.stop()
value = lock_in_amp.read_buffer_data(1, 0, 50)
print(value[1])
value = lock_in_amp.read_buffer_data(2, 0, 50)
print(value[1])