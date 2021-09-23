from intelhex import IntelHex
import sys

sourceFile = './code.asm'
outputFile = './out.hex'
if len(sys.argv) >= 2:
  sourceFile = sys.argv[1]
if len(sys.argv) >= 3:
  outputFile = sys.argv[2]

humanCode = open(sourceFile, 'r')
lines = humanCode.readlines()

instructionMap = {
  'nop': 0,

  # REGISTERS
  'ima': 2,
  'exa': 3,
  'lia': 4,

  'imb': 7,
  'exb': 8,
  'lib': 9,
  
  'imc': 12,
  'exc': 13,
  'lic': 14,

  # BRANCHES
  'jmp': 32,
  'jmz': 33,
  'jmc': 35,

  # OPERATIONS
  'add': 64,

  # IO
  'out': 128
}

class ParseError(Exception):
  def __init__(self, msg):
    print('parse err', msg)

class InvalidInstructionError(Exception): pass

def parseLine(line):
  global lines
  name = ''
  argument = ''
  mode = 'name'
  for i,c in enumerate(line):
    if c == '#':
      if i > 0:
        break
      else:
        return None
    if c == ' ':
      if mode == 'name':
        mode = 'argument'
      elif mode == 'argument':
        mode = 'name'
      continue
    if c == "\n":
      break

    if mode == 'name': name += c
    if mode == 'argument': argument += c
  # parse argument
  if argument.startswith('0x'):
    argument = int(argument.replace('0x', ''), 16)
  elif argument.startswith('0b'):
    argument = int(argument.replace('0b', ''), 2)

  name = name.lower()
  if name == '':
    return None
  return (name, argument)

def parse(lines):
  instructions = []
  for line in lines:
    parsedLine = parseLine(line)
    if parsedLine == None: continue
    instructions.append(parsedLine)
  return instructions

instructions = parse(lines)
print(instructions)

realCode = []
ih = IntelHex()
addr = 0
for (name, arg) in instructions:
  if name not in instructionMap:
    print(name)
    raise InvalidInstructionError()
  name = instructionMap[name]
  ih[addr] = name
  addr += 1
  arg = int(arg) if type(arg) is int or arg.isnumeric() else 0
  ih[addr] = arg
  realCode.append((name, arg))
  addr += 1

ih.write_hex_file(outputFile)
print(realCode)
