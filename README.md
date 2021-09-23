# WIP: 8 bit computer

This version isn't actually working, I have issues when running the simulation:

it errors randomly :

```
Error calculating a step
More than one output is active on a wire, causing a short circuit.
```

Highlighting the DBUS (main 8-bit bus) wire

## How to use

- clone the repository
- open "computer.dig" in [Digital](https://github.com/hneemann/Digital)
- change the path of the program ROM and the 3 7-segment display decoder ROM 
- you're good to go
- use the script `compile.py ./your-source.asm ./out.hex` to compile assembler into binary

## Achitectures

- 8-bit bus called "DBUS"
- each instruction is two bytes long (opcode + argument) and stored at 2 ajacent address in ROM
- A, B and C register

- 2 bit micro step counter called "IC" for Internal Counter
- 8 bit program counter called "PC"

## Instructions

- 0. NOP
  - desc: no operation
  - arg: (empty)

### Registers (0-32)

- 2. IMA
  - desc: import from memory to A register
  - arg: memory address to load
  - flags:
    - MREAD
    - ASTORE
    - AR <-> MADDR

- 3. EXA
  - desc: export data that A register has into memory
  - arg: memory address to store
  - flags:
    - MSTORE
    - AREAD
    - AR <-> MADDR

- 4. LIA
  - desc: load immediate value into A register
  - arg: the value to load
  - flags:
    - ASTORE

same for B (7, 8, 9) and C register (also called output register) (12, 13, 14)

### Branches (32-64)

- 32. JMP:
  - desc: unconditional jump
  - arg: address in ROM to jump to
  - flags:
    - PCSET
    - AR <-> DBUS

- 35. JMC:
  - desc: jump if adder carry flag is set
  - arg: address in ROM to jump to
  
- 36. JMZ: (not implemented)
  - desc: jump if C register is zero
  - arg: address in ROM to jump to

- 37. JMA: (not implemented)
  - desc: jump if C register is 255
  - arg: address in ROM to jump to

- 63. HLT:
  - desc: halt execution of the processing unit
  - implementation: will keep reseting the Program counter
  - arg: (empty)

### Operations (64-128)

- 64. ADD:
  - desc: add the two numbers in register A and B and put result in C
  - arg: no arg

- 65. AND: (not implemented)
  - desc: apply AND bitwise operation to A and B and put result in C
  - arg: (empty)

- 66. IOR: (not implemented)
  - desc: apply OR bitwise operation to A and B and put result in C
  - arg: (empty)

- 67. XOR: (not implemented)
  - desc: apply XOR bitwise operation to A and B and put result in C
  - arg: (empty)

- 68. SHL: (not implemented)
  - desc: shift left one bit A and put result in C
  - arg: (empty)

- 69. SHR: (not implemented)
  - desc: shift right one bit A and put result in C
  - arg: (empty)

### I/O (128-256)

- 128. OUT:
  - desc: output content of A register to 7 seg displays
  - arg: (empty)
