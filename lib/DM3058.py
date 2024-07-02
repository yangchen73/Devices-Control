import pyvisa

class DM3058:
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
            print("DM3058 connected successfully.")
        else:
            raise ValueError("Failed to connect to DM3058.")


        self.instrument.timeout = 2000
    def reset(self):
        """重置万用表"""
        self.instrument.write("*RST")

    def close(self):
        """关闭与万用表的连接"""
        self.instrument.close()

    def get_id(self):
        """获取万用表的身份识别字符串"""
        return self.instrument.query("*IDN?").strip("\n")

    def set_function(self, function, mode=None):
        """Set the current measurement function.

        Parameters
        ----------
        function : str
            Measurement function: voltage, current, resistance, frequency, period,
            continuity, diode, or capacitance.
        mode : str or None
            Mode of the measurement function. The valid modes for each function that
            has multiple modes are:
                voltage: dc (defualt), ac
                current: dc (defualt), ac
                resistance: 2-wire (defualt), 4-wire

            If `None`, the default mode is selected.
        """
        cmd = ":FUNC"

        if function == "voltage":
            cmd += ":VOLT"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid voltage mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "current":
            cmd += ":CURR"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid current mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "resistance":
            if (mode is None) or (mode == "2-wire"):
                cmd += ":RES"
            elif mode == "4-wire":
                cmd += ":FRES"
            else:
                raise ValueError(
                    f"Invalid resistance mode: {mode}. Must be '2-wire' or '4-wire'."
                )
        elif function == "frequency":
            cmd += ":FREQ"
        elif function == "period":
            cmd += ":PER"
        elif function == "continuity":
            cmd += ":CONT"
        elif function == "diode":
            cmd += ":DIOD"
        elif function == "capacitance":
            cmd += ":CAP"
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', 'current', "
                + "'resistance', 'frequency', 'period', 'continuity', 'diode', or "
                + "'capacitance'."
            )

        self.instrument.write(cmd)

    def measure(self, function, mode):
        """Perform a measurement using the selected function.

        Parameters
        ----------
        function : str
            Measurement function: voltage, current, resistance, frequency, period,
            continuity, diode, or capacitance.
        mode : str or None
            Mode of the measurement function. The valid modes for each function that
            has multiple modes are:
                voltage: dc (defualt), ac
                current: dc (defualt), ac
                resistance: 2-wire (defualt), 4-wire

            If `None`, the default mode is selected.
        """
        cmd = ":MEAS"

        if function == "voltage":
            cmd += ":VOLT"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC?"
            elif mode == "ac":
                cmd += ":AC?"
            else:
                raise ValueError(f"Invalid voltage mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "current":
            cmd += ":CURR"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC?"
            elif mode == "ac":
                cmd += ":AC?"
            else:
                raise ValueError(f"Invalid current mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "resistance":
            if (mode is None) or (mode == "2-wire"):
                cmd += ":RES?"
            elif mode == "4-wire":
                cmd += ":FRES?"
            else:
                raise ValueError(
                    f"Invalid resistance mode: {mode}. Must be '2-wire' or '4-wire'."
                )
        elif function == "frequency":
            cmd += ":FREQ?"
        elif function == "period":
            cmd += ":PER?"
        elif function == "continuity":
            cmd += ":CONT?"
        elif function == "diode":
            cmd += ":DIOD?"
        elif function == "capacitance":
            cmd += ":CAP?"
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', 'current', "
                + "'resistance', 'frequency', 'period', 'continuity', 'diode', or "
                + "'capacitance'."
            )

        return float(self.instr.query(cmd).strip("\n"))

# 使用示例
if __name__ == "__main__":
    resource_name = 'USB0::0x1AB1::0x09C4::DM3L195201332::INSTR'
    multimeter = DM3058(resource_name)
    print("Multimeter ID:", multimeter.get_id())
    multimeter.set_function('voltage', 'dc')
    voltage = multimeter.measure('voltage', 'dc')
    print("Measured voltage:", voltage, "V")