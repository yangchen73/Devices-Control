import pyvisa

class IT6322A:
    def __init__(self, resource_name, reset=True):
        """
        初始化IT6322A直流电源。
        :param resource_name: VISA资源名称, 比如说USB地址 'USB0::0x0699::0x03A2::C040194::INSTR'
        :param reset: 是否重置万用表到出厂默认设置, 这里默认重置
        """
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_name)
        if reset:
            self.reset()
        # 检查连接
        if "ITECH" in self.get_id():
            print("IT6322A connected successfully.")
        else:
            raise ValueError("Failed to connect to IT6322A.")

    def get_id(self):
        """获取万用表的身份识别字符串"""
        return self.instrument.query("*IDN?").strip()

    def reset(self):
        """将直流电源重置为出厂默认设置"""
        self.instrument.write("*RST")

    def close(self):
        """关闭直流电源的连接"""
        self.instrument.close()

    def set_voltage(self, channel, voltage):
        """
        设置指定通道的电压级别。
        """
        cmd = f"SOURce:CHANnel{channel}"
        self.instrument.write(cmd)
        cmd = f"SOURce:VOLTage {voltage}"
        self.instrument.write(cmd)

    def set_current(self, channel, current):
        """
        设置指定通道的电流级别。
        """
        cmd = f"SOURce:CHANnel{channel}"
        self.instrument.write(cmd)
        cmd = f"SOURce:CURRent {current}"
        self.instrument.write(cmd)

    def output_on(self, channel):
        """
        打开指定通道的输出。
        """
        self.select_channel(channel)  # 选择通道
        self.instrument.write("OUTPut ON")

    def output_off(self, channel):
        """
        关闭指定通道的输出。
        """
        self.select_channel(channel)  # 选择通道
        self.instrument.write("OUTPut OFF")

    def get_voltage(self, channel):
        """
        测量指定通道的电压。

        :param channel: 通道号 (1, 2, 或 3)
        :return: 测量到的电压值
        """
        cmd = f"MEASure:VOLTage:DC? CH{channel}"
        return float(self.instrument.query(cmd))

    def get_current(self, channel):
        """
        测量指定通道的电流。

        :param channel: 通道号 (1, 2, 或 3)
        :return: 测量到的电流值
        """
        cmd = f"MEASure:CURRent:DC? CH{channel}"
        return float(self.instrument.query(cmd))

# 使用示例
if __name__ == "__main__":
    resource_name = "USB0::0xFFFF::0x6300::602071010727630016::INSTR" 
    power_supply = IT6322A(resource_name, reset=True)
    power_supply.output_on(1) 
    power_supply.set_voltage(1, 5)  # 在通道1上设置电压为5V
    power_supply.set_current(1, 1) 
    print(f"Voltage: {power_supply.get_voltage(1)}V")
    print(f"Current: {power_supply.get_current(1)}A")
    power_supply.output_off(1)  
    power_supply.close()