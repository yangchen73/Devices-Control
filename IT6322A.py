import pyvisa

class IT6322A:
    def __init__(self, resource_name):
        # 连接
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_name)
        
        # 设置超时时间
        self.instrument.timeout = 5000  # 5秒

        # 检查连接
        if "ITECH" in self.instrument.query("*IDN?"):
            print("IT6322A connected successfully.")
        else:
            raise ValueError("Failed to connect to IT6322A.")

    def set_voltage(self, channel, voltage):
        self.instrument.write(f"SOURce{channel}:VOLTage {voltage}")

    def set_current(self, channel, current):
        self.instrument.write(f"SOURce{channel}:CURRent {current}")

    def output_on(self, channel):
        self.instrument.write(f"SOURce{channel}:OUTPut ON")

    def output_off(self, channel):
        self.instrument.write(f"SOURce{channel}:OUTPut OFF")

    def get_voltage(self, channel):
        return float(self.instrument.query(f"SOURce{channel}:MEASure:VOLTage:DC?"))

    def get_current(self, channel):
        return float(self.instrument.query(f"SOURce{channel}:MEASure:CURRent:DC?"))

    def close(self):
        self.instrument.close()
        self.rm.close()

# 使用示例
if __name__ == "__main__":
    
    power_supply = IT6322A('')
    power_supply.set_voltage(1, 5)  # 设置通道1电压为5V
    power_supply.set_current(1, 0.1)  # 设置通道1电流为0.1A
    power_supply.output_on(1)  # 开启通道1输出
    # 读取并打印通道1的电压和电流
    print(f"Voltage: {power_supply.read_voltage(1)} V")
    print(f"Current: {power_supply.read_current(1)} A")
    power_supply.output_off(1)  
    power_supply.close()  