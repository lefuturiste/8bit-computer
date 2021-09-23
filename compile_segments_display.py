from intelhex import IntelHex

digits = [
  0x7E,
  0x30,
  0x6D,
  0x79,
  0x33,
  0x5B,
  0x5F,
  0x70,
  0x7F,
  0x7B
]

# map from 0 to 255
# display number 0 is the right
# display number 1 is the middle
# display number 2 is the left
for i in range(3):
  ih = IntelHex()
  for j in range(256):
    s = list(reversed(str(j).zfill(3)))
    ih[j] = digits[int(s[i])]
  ih.write_hex_file("seg_display_" + str(i) + ".hex")

