meta:
  id: pmd2pack
  endian: le
  file-extension: bin
    
seq:
  - id: buffer
    type: u4
  - id: file_count
    type: u4
  - id: files
    type: file
    repeat: expr
    repeat-expr: file_count
  
types:
  file:
    seq:
      - id: pointer
        type: u4
      - id: length
        type: u4
    instances:
      data:
        pos: pointer
        size: length