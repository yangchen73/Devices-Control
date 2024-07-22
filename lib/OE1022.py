import serial
import time

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

    def query_phase(self):
        """
        查询相位
        """
        return self.send_command("PHAS?")
    
    def get_id(self):
        return self.send_command("*IDN?")

    def query_output_parameter(self, param_code):
        """
        使用OUTP?i命令查询特定的输出参数值
        param_code: 参数代码，对应不同的输出值
                    例如 1: X, 2: Y, 3: R, 4: θ, 等
        """
        command = f"OUTP?{param_code}\r"
        response = self.send_command(command)
        return response
    def read_buffer_data(self, buffer_num, start_index, length):
            """
            使用 TRCA? i, j, k 命令读取数据缓存区的数据
            buffer_num: 缓存区编号 (1-4)
            start_index: 起始索引（从哪个数据点开始读取）
            length: 要读取的数据长度
            """
            command = f"TRCA? {buffer_num}, {start_index}, {length}\r"
            response = self.send_command(command)         
            return response


# 使用示例
if __name__ == "__main__":
    lock_in_amp = OE1022('/dev/cu.usbserial-110')  # 替换为您的设备对应的COM端口

    buffer_data = lock_in_amp.read_buffer_data(1, 0, 10)
    print(f"Buffer Data: {buffer_data}")
    phase = lock_in_amp.query_phase()
    print(lock_in_amp.query_output_parameter(4))

