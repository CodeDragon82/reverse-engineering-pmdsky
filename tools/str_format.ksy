meta:
  id: str_format
  endian: le
  encoding: windows-1252
  file-extension: str

seq:
  - id: strings
    type: string_pointer
    repeat: until
    repeat-until: _.offset >= _io.size - 1
    
types:
  string_pointer:
    seq:
      - id: offset
        type: u4
        
    instances:
      string:
        pos: offset
        type: strz