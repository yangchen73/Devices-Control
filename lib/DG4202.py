import pyvisa


class DG4202:
    def __init__(self, resource_name, reset=True):
        self.rm = pyvisa.ResourceManager()
        self.waveform = self.rm.open_resource(resource_name)
        if reset:
            self.reset()

    def reset(self):
        self.waveform.write("*RST")

    def get_id(self):
        identity = self.waveform.query("*IDN?").strip()
        return identity

    def wave_output_state(self,output_state=0):
        self.waveform.write(f'OUTPut:STATe {output_state}')
        print('waveform output state= ',self.waveform.query(':OUTPut:STATe?'))

    def apply_sine_wave(self, channel, freq, amp=5, offset=0, phase=0):
        command = f":SOURce{channel}:APPLy:SINusoid {freq},{amp},{offset},{phase}"
        self.waveform.write(command)

    def set_output_state(self, channel, state):
        """
        使用SCPI命令设置指定通道的输出状态。

        :param instrument: 与仪器通信的SCPI接口对象。
        :param channel: 通道编号，例如1或2。
        :param state: 输出状态，'ON' 或 'OFF'。
        """
        # 检查状态参数是否有效
        if state not in ['ON', 'OFF']:
            raise ValueError("Invalid state. Must be 'ON' or 'OFF'.")

        # 构建并发送SCPI命令
        command = f":OUTPut{channel}:STATe {state}"
        self.waveform.write(command)


if __name__ == "__main__":
    resource_name = 'USB0::0x1AB1::0x0641::DG4E195204310::INSTR'
    generator = DG4202(resource_name)

    generator.apply_sine_wave(1, 120, 5.5, 1.5, 90)
    generator.set_output_state(1,'ON')