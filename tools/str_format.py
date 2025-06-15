# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class StrFormat(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.strings = []
        i = 0
        while True:
            _ = StrFormat.StringPointer(self._io, self, self._root)
            self.strings.append(_)
            if _.offset >= (self._io.size() - 1):
                break
            i += 1

    class StringPointer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()

        @property
        def string(self):
            if hasattr(self, '_m_string'):
                return self._m_string

            _pos = self._io.pos()
            self._io.seek(self.offset)
            self._m_string = (self._io.read_bytes_term(0, False, True, True)).decode(u"windows-1252")
            self._io.seek(_pos)
            return getattr(self, '_m_string', None)



