
f = open("hexcode.hex", "wb")
a = bytearray([0x42, 0x41, 0x65, 0xA])
f.write(a)
