import time
from lib.OE1022 import OE1022

lock_in_amp = OE1022('/dev/cu.usbserial-120')
lock_in_amp.reset()     
lock_in_amp.set_harmonic(1,1)
lock_in_amp.set_harmonic(2,2)

lock_in_amp.set_buffer_selection(1, 'Yh1')
lock_in_amp.set_buffer_selection(2, 'Xh2')

lock_in_amp.get_start()
time.sleep(3)
lock_in_amp.stop()
value = lock_in_amp.read_buffer_data(1, 0, 50)
print(value[1:len(value)-1])
mean, variance, std_deviation = lock_in_amp.calculate_statistics(value[1:len(value)-1])
print('mean=',mean, 'variance=',variance, 'std_deviation=',std_deviation)
# print (value[1:len(value)-1])
# print(value[1:len(value)-2])

value = lock_in_amp.read_buffer_data(2, 0, 50)
mean, variance, std_deviation = lock_in_amp.calculate_statistics(value[1:len(value)-1])
print('mean=',mean, 'variance=',variance, 'std_deviation=',std_deviation)
