# 1, 1, 2, 3, 5, 8 etc
# FIBONACCI SEQUENCE
section init:
  nop
  nop
  nop
  nop
  nop
  lia 1 # old
  lib 1 # new
  lic 0

  out

  exa 1
  exb 2

section loop:
  # add old and new
  ima 1
  imb 2
  add

  # reset if carry
  jmc @init

  # exchange old and new
  imc 2
  exc 1

  # put back the result into new
  exb 2

  out

  nop

  # loop back
  jmp @loop
