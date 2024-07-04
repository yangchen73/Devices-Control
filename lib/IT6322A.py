import pyvisa
import time

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

    def select_channel(self, channel):
        """
        切换到指定的通道。
        :param channel: 通道号，可以是 'CH1', 'CH2' 或 'CH3'
        """
        if channel in ('CH1', 'CH2', 'CH3'):
            cmd = f"INSTrument:SELect {channel}"
            self.instrument.write(cmd)
        else:
            raise ValueError("Invalid channel. Must be 'CH1', 'CH2', or 'CH3'.")
        
    def set_voltage(self, channel, voltage):
        """
        设置指定通道的电压级别。
        """
        self.select_channel(channel)
        cmd = f"SOURce:VOLTage {voltage:.3f}"  # 保留两位小数
        self.instrument.write(cmd)
        

    def set_current(self, channel, current):
        """
        设置指定通道的电流级别。
        """
        self.select_channel(channel)
        cmd = f"SOURce:CURRent {current:.3f}"  # 保留两位小数
        self.instrument.write(cmd)
    def output_on(self):
        """
        打开指定通道的输出。
        """
        self.instrument.write("OUTPut ON")

    def output_off(self, channel):
        """
        关闭指定通道的输出。
        """
        cmd = f"SOURce:CHANnel{channel}"
        self.instrument.write(cmd)  # 选择通道
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

    resource_name = 'USB0::0xFFFF::0x6300::602071010727730104::INSTR'
    power_supply = IT6322A(resource_name)
    power_supply.output_on()


    for voltage in range(0, 7, 1):
        power_supply.set_voltage('CH2', voltage)
        time.sleep(1)
            
            