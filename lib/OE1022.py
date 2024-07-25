import serial
import time
import math

class OE1022:
    def __init__(self, port, baudrate=921600, timeout=0.01):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def send_command(self, command):
        """
        发送命令到锁相放大器并读取响应
        """
        self.ser.write((command + '\r').encode())
        response = self.ser.readline().decode().strip()
        return response

    def get_id(self):
        return self.send_command("*IDN?")
    def reset(self):
        self.send_command("REST")

    def query_output_parameter(self, param_code):
        """
        使用OUTP?i命令查询特定的输出参数值
        param_code: 参数代码，对应不同的输出值
                    例如 1: X, 2: Y, 3: R, 4: θ, 等
        """
        command = f"OUTP?{param_code}\r"
        response = self.send_command(command)
        return response
    def get_start(self):
        self.send_command("STRD")

    def set_buffer_selection(self, buffer_num, parameter):
        command = f"SSLE {buffer_num}, {parameter}\r"
        return self.send_command(command)
    
    def read_buffer_data(self, buffer_num, start_index, length):
        """
        使用 TRCA? i, j, k 命令读取数据缓存区的数据，并计算平均值
        buffer_num: 缓存区编号 (1-4)
        start_index: 起始索引（从哪个数据点开始读取）
        length: 要读取的数据长度
        """
        command = f"TRCA? {buffer_num}, {start_index}, {length}\r"
        response = self.send_command(command)
        data_points = response.split(',')
        data_values = [float(point) for point in data_points]
        return data_values

def calculate_statistics(data_values):
    """
    计算数据的平均值、方差和标准差
    :param data_values: 数据列表
    :return: 平均值、方差、标准差
    """
    n = len(data_values)
    if n == 0:
        return None, None, None

    mean = sum(data_values) / n
    variance = sum((x - mean) ** 2 for x in data_values) / n
    std_deviation = math.sqrt(variance)
    return mean, variance, std_deviation

if __name__ == "__main__":
    lock_in_amp = OE1022('/dev/cu.usbserial-110')  
    lock_in_amp.reset()
    lock_in_amp.set_buffer_selection(1, 'θ')
    lock_in_amp.get_start()
    time.sleep(3)
    value = lock_in_amp.read_buffer_data(1, 0, 50)
    print(calculate_statistics(value))
