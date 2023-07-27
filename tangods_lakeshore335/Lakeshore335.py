#!/usr/bin/python3 -u
# coding: utf8
# Lakeshore335

from tango import AttrQuality, AttrWriteType, DispLevel, DevState, DebugIt
from tango.server import Device, attribute, command, pipe, device_property

from serial import Serial, PARITY_ODD, STOPBITS_ONE
import time
from enum import IntEnum


class HeaterRange(IntEnum):
    off = 0
    low = 1
    medium = 2
    high = 3


class Lakeshore335(Device):
    Port = device_property(dtype=str, default_value="/dev/ttyLakeshore")

    Baudrate = device_property(dtype=int, default_value=57600)

    Output = device_property(dtype=int, default_value=1, doc="output 1 or 2")

    inputa = attribute(
        label="input A",
        dtype=float,
        unit="K",
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        doc="input A temperature",
    )

    inputb = attribute(
        label="input B",
        dtype=float,
        unit="K",
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        doc="input B temperature",
    )

    output = attribute(
        label="output",
        dtype=int,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        doc="output",
    )

    setpoint = attribute(
        label="setpoint",
        dtype=float,
        unit="K",
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ_WRITE,
        doc="setpoint",
    )

    heater_range = attribute(
        dtype=HeaterRange,
        label="heater range",
        access=AttrWriteType.READ_WRITE,
        display_level=DispLevel.OPERATOR,
    )

    heater_output = attribute(
        dtype=float,
        unit="%",
        format="%4.1f",
        label="heater output",
        access=AttrWriteType.READ,
        display_level=DispLevel.OPERATOR,
    )

    def init_device(self):
        Device.init_device(self)

        self.con = Serial(
            port=self.Port,
            baudrate=self.Baudrate,
            timeout=3,
            parity=PARITY_ODD,
            stopbits=STOPBITS_ONE,
            bytesize=7,
        )

        if self.con.isOpen():
            self.set_state(DevState.ON)
            self.info_stream("Initialised on port {:s}".format(self.con.port))
            self.info_stream("Connected to device {:s}".format(self.write("*IDN?")))
        else:
            self.error_stream("Cannot connect on port {:s}".format(self.con.port))

    # attributes
    def read_inputa(self):
        return float(self.write("KRDG?A"))

    def read_inputb(self):
        return float(self.write("KRDG?B"))

    def read_output(self):
        return int(self.Output)

    def read_setpoint(self):
        return float(self.write("SETP? {:d}".format(self.Output)))

    def write_setpoint(self, value):
        self.write("SETP {:d},{:f}".format(self.Output, value))

    def read_heater_range(self):
        return int(self.write("RANGE? {:d}".format(self.Output)))

    def write_heater_range(self, value):
        self.write("RANGE {:d},{:d}".format(self.Output, value))

    def read_heater_output(self):
        return float(self.write("HTR? {:d}".format(self.Output)))

    # commands
    @command(
        dtype_in=str,
        doc_in="enter a command",
        dtype_out=str,
        doc_out="response from a query",
    )
    def write(self, cmd):
        self.debug_stream(cmd)
        cmd = cmd + "\r\n"
        ans = self.con.write(cmd.encode("utf-8"))
        if cmd.find("?") >= 0:
            # it is a query
            time.sleep(0.02)
            return self.con.readline().decode("utf-8")
        else:
            # it is a command
            return ""

    @command(dtype_in=int, doc_in="Select input for control loop")
    def loop_select_input(self, input):
        if input in [0, 1, 2]:
            self.write("OUTMODE {:d},1,{:d},0".format(self.Output, input))
        else:
            self.warning_stream("Inout must be 0=None, 1=Input A, 2=Input B")

    @command(dtype_in=(float,), doc_in="ramp enable 0/1 and rate in K/min")
    def ramp(self, value):
        enable, ramp = value
        self.write("OUTMODE {:d},{:d},{:f}".format(self.Output, int(enable), abs(ramp)))


if __name__ == "__main__":
    Lakeshore335.run_server()
