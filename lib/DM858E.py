import pyvisa
import time

class DM858E:
    def __init__(self, resource_name, reset=True):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_name)
        
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
        """Set the current measurement function.

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

        return float(self.instrument.query(cmd).strip())


if __name__ == "__main__":
    resource_name ='USB0::0x1AB1::0x210B::DM8E260300157::INSTR'
    multimeter = DM858E(resource_name)
    print(multimeter.measure('voltage','dc'))


