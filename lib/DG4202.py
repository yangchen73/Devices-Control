import pyvisa

class waveform_generator:
    def __init__(self, instrument_address, reset=True):
        self.rm = pyvisa.ResourceManager()
        self.instrument_address = instrument_address
        self.waveform = self.rm.open_resource(instrument_address)
        if reset:
            self.reset()
        self.check_connection()

    def reset(self):
        self.waveform.write("*RST")

    def check_connection(self):
        identity = self.waveform.query("*IDN?").strip()
        print(f"Connected to: {identity}")

    def wave_set(self,channel_idx=1,waveform_type='SIN',amp_vpp=200,apm_offset=100,
                     phase = 0,out_load=50,freq=5000):
        # waveform_type='SIN'  # SCPI: FUNCtion {SIN|SQU|RAMP|PULSe|NOIS|DC|PRBS|ARB}
        self.waveform.write(f'CHANnel{channel_idx}:FUNCtion {waveform_type}')
        # 设置波形类型
        self.waveform.write(f'FUNCtion {waveform_type}')
        # 设置频率
        self.waveform.write(f'FREQ {freq} Hz')
        # 设置峰峰电压
        self.waveform.write(f'VOLTage:PEAKtoPEAK {amp_vpp} mV')
        # 设置偏置电压
        self.waveform.write(f'VOLT:OFFS {apm_offset} mV')
        # 设置相位
        self.waveform.write(f'PHASe {phase} deg')
        # 设置输出阻抗
        self.waveform.write(f'OUTPut:LOAD {out_load}')        # print(f'CHANnel{channel_idx} OUTPut[1|2]:LOAD =', self.waveform.query('OUTPut:LOAD?'))
 
    def wave_output_state(self,output_state=0):
        self.waveform.write(f'OUTPut:STATe {output_state}')
        print('waveform output state= ',self.waveform.query(':OUTPut:STATe?'))