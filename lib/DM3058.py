import pyvisa

class DP3058:
    def __init__(self, resource_name, reset=True):
        """
        初始化DP3058万用表。
        :param resource_name: VISA资源名称, 比如说USB地址 'USB0::0x0699::0x03A2::C040194::INSTR'
        :param reset: 是否重置万用表到出厂默认设置, 这里默认重置
        """
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_name)

        if reset:
            self.reset()
        # 检查连接
        if "RIGOL" in self.get_id():
            print("DP3058 connected successfully.")
        else:
            raise ValueError("Failed to connect to DP3058.")

    def reset(self):
        """重置万用表"""
        self.instrument.write("*RST")

    def close(self):
        """关闭与万用表的连接"""
        self.instrument.close()

    def get_id(self):
        """获取万用表的身份识别字符串"""
        return self.instrument.query("*IDN?").strip()

    def set_function(self, function, mode=None):
        """
        设置测量功能及其模式。
        
        :param function: 测量功能，例如 'voltage'（电压）, 'current'（电流）, 'resistance'（电阻）
        :param mode: 测量功能的模式，例如 'dc'（直流）, 'ac'（交流）, '2-wire'（二线制）, '4-wire'（四线制）
        """
        cmd = f":FUNC{function.upper()}"

        if function in ["voltage", "current"] and mode in [None, "dc", "ac"]:
            cmd += f":{mode.upper()}"
        elif function == "resistance" and mode in [None, "2-wire", "4-wire"]:
            cmd += f":{mode.replace('2-wire', 'RES').replace('4-wire', 'FRES').upper()}"
        else:
            raise ValueError("Invalid function or mode specified.")

        self.instrument.write(cmd)

    def measure(self, function, mode=None):
        """
        使用选定的功能和模式进行测量。
        
        :param function: 测量功能，例如 'voltage'（电压）, 'current'（电流）, 'resistance'（电阻）
        :param mode: 测量功能的模式，例如 'dc'（直流）, 'ac'（交流）, '2-wire'（二线制）, '4-wire'（四线制）
        :return: 测量得到的数值
        """ 
        self.set_function(function, mode)
        return float(self.instrument.query(f":MEAS{function.upper()}?").strip())

# 使用示例
if __name__ == "__main__":
    resource_name = "'USB0::0x0699::0x03A2::C040194::INSTR'" 
    multimeter = DP3058(resource_name, reset=True)
    print("Multimeter ID:", multimeter.get_id())
    voltage = multimeter.measure('voltage', 'dc')
    print("Measured voltage:", voltage, "V")
    multimeter.close()