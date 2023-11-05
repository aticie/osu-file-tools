import struct
from typing import IO


class Reader:
    def __init__(self, file_io: IO):
        self.buffer = file_io

    def read_bool(self) -> bool:
        return struct.unpack("<?", self.buffer.read(1))[0]

    def read_ubyte(self) -> int:
        return struct.unpack("<B", self.buffer.read(1))[0]

    def read_ushort(self) -> int:
        return struct.unpack("<H", self.buffer.read(2))[0]

    def read_uint(self) -> int:
        return struct.unpack("<I", self.buffer.read(4))[0]

    def read_float(self) -> float:
        return struct.unpack("<f", self.buffer.read(4))[0]

    def read_double(self) -> float:
        return struct.unpack("<d", self.buffer.read(8))[0]

    def read_ulong(self) -> int:
        return struct.unpack("<Q", self.buffer.read(8))[0]

    # osu specific
    def read_int_double(self):
        self.read_ubyte()
        integer = self.read_uint()
        self.read_ubyte()
        double = self.read_double()
        return integer, double

    def read_timing_point(self):
        bpm = self.read_double()
        offset = self.read_double()
        inherited = self.read_bool()
        return bpm, offset, inherited


    def read_string(self) -> str:
        strlen = 0
        strflag = self.read_ubyte()
        if strflag == 0x0b:
            strlen = 0
            shift = 0
            while True:
                byte = self.read_ubyte()
                strlen |= ((byte & 0x7F) << shift)
                if (byte & (1 << 7)) == 0:
                    break
                shift += 7
        return (struct.unpack("<" + str(strlen) + "s", self.buffer.read(strlen))[0]).decode("utf-8")


class WriteBuffer:
    def __init__(self):
        self.offset = 0
        self.data = b""

    def write_bool(self, data: bool):
        self.data += struct.pack("<?", data)

    def write_ubyte(self, data: int):
        self.data += struct.pack("<B", data)

    def write_ushort(self, data: int):
        self.data += struct.pack("<H", data)

    def write_uint(self, data: int):
        self.data += struct.pack("<I", data)

    def write_float(self, data: float):
        self.data += struct.pack("<f", data)

    def write_double(self, data: float):
        self.data += struct.pack("<d", data)

    def write_ulong(self, data: int):
        self.data += struct.pack("<Q", data)

    def write_string(self, data: str):
        if len(data) > 0:
            self.write_ubyte(0x0b)
            strlen = b""
            value = len(data.encode())
            while value != 0:
                byte = (value & 0x7F)
                value >>= 7
                if value != 0:
                    byte |= 0x80
                strlen += struct.pack("<B", byte)
            self.data += strlen
            self.data += struct.pack("<" + str(len(data)) +
                                     "s", data.encode("utf-8"))
        else:
            self.write_ubyte(0x0)

    def clear_buffer(self):
        self.data = b""
