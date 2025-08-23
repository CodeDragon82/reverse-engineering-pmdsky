# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Pkdpx(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(5)
        if not self.magic == b"\x50\x4B\x44\x50\x58":
            raise kaitaistruct.ValidationNotEqualError(b"\x50\x4B\x44\x50\x58", self.magic, self._io, u"/seq/0")
        self.length = self._io.read_u2le()
        self.controls_flags = self._io.read_bytes(9)
        self.decompressed_length = self._io.read_u4le()
        self.data = self._io.read_bytes((self.length - 20))


