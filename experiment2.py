import pyvisa
import serial.tools.list_ports

def list_resources():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

def list_serial_ports():
    """
    列出当前系统上所有的串行端口。
    """
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")

if __name__ == "__main__":
    list_resources()
    list_serial_ports()