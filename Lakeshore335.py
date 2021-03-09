#!/usr/bin/python3 -u
# coding: utf8
# Lakeshore335

from tango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

from serial import Serial, PARITY_ODD, STOPBITS_ONE


class Lakeshore335(Device):

    Port = device_property(
        dtype=str,
        default_value='/dev/ttyLakeshore'
    )
    
    Baudrate = device_property(
        dtype=int,
        default_value=57600
    )
    
    # Useful strings:
    CR        = chr(13)   #carrier Return - needs to be send at the end of each line
    enable    = 'ens'
    isEnabled = 'ens?'

    inputA = attribute(label="input A", dtype=float,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         doc="input A temperature",)
    
    inputB = attribute(label="input B", dtype=float,
                         display_level=DispLevel.OPERATOR,
                         access=AttrWriteType.READ,
                         doc="input B temperature",)

    def init_device(self):
        Device.init_device(self)
        
        self.con = Serial(port=self.Port, baudrate=self.Baudrate,
                          timeout=3, parity = PARITY_ODD,
                          stopbits = STOPBITS_ONE, bytesize = 7)
)
        if self.connection.isOpen():
            self.set_state(DevState.ON)
            self.info_stream('Initialised on port {:s}.'.format(self.connection.port))

    # commands
    @command(self, dtype_in=str, doc_in="enter a command")
    def write(connection, cmd):
        cmd = cmd + '\r\n'   #\n does not work.
        ans = self.con.write(cmd.encode("utf-8"))

    @command(self, dtype_out=str, doc_out="response from a command")        
    def read(self):
        return self.con.readline().decode("utf-8")


if __name__ == "__main__":
    Lakeshore335.run_server()
