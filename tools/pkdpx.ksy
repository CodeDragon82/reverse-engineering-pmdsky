meta:
  id: pkdpx
  endian: le
  file-extension: pkdpx
  
seq:
  - id: magic
    contents: "PKDPX"
  - id: length
    type: u2
  - id: controls_flags
    size: 9
  - id: decompressed_length
    type: u4
  - id: data
    size: length - 20