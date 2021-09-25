# multiply number in reg a and b
section init:
  # load inputs
  lia 42
  exa 1
  exa 4

  lib 3
  exb 2

  lia 1
  exa 3

  lic 0

section multiply:
  # address layout:
  # 1: a: to add each time
  # 2: b: max nb of operation
  # 3: number of operations
  # 4: current result
  ima 4
  imb 1
  add
  exb 4

   # increment nb operations by 1
  ima 3
  lib 1
  add
  exb 3

  #imc 3

  # check if nb of operations are done
  ima 2
  imb 3
  
  jnq @multiply

  # output result
  imb 4
  out

  hlt