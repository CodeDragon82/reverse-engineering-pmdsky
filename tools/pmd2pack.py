# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import BytesIO, KaitaiStream, KaitaiStruct

if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Pmd2pack(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.buffer = self._io.read_u4le()
        self.file_count = self._io.read_u4le()
        self.files = []
        for i in range(self.file_count):
            self.files.append(Pmd2pack.File(self._io, self, self._root))


    class File(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pointer = self._io.read_u4le()
            self.length = self._io.read_u4le()

        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data

            _pos = self._io.pos()
            self._io.seek(self.pointer)
            self._m_data = self._io.read_bytes(self.length)
            self._io.seek(_pos)
            return getattr(self, '_m_data', None)



