from intelhex import IntelHex
import sys
import re

sourceFile = './code.asm'
outputFile = './out.hex'
if len(sys.argv) >= 2:
  sourceFile = sys.argv[1]
if len(sys.argv) >= 3:
  outputFile = sys.argv[2]

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
  'jmc': 35,
  'jmz': 36,
  'jnq': 37,
  'hlt': 63,

  # OPERATIONS
  'add': 64,

  # IO
  'out': 128
}

class ParseError(Exception):
  def __init__(self, msg, lineIndex = -1):
    print(f'PARSE ERROR: {msg} at line {lineIndex+1}')
    exit()

class InvalidInstructionError(Exception): pass

def removeComment(inp):
  out = ''
  for c in inp:
    if c == '#':
      return out
    out += c
  return out

def parseSections(rawLines):
  sections = []
  # pre parse sections
  sectionRegex = r"section (?P<NAME>[0-9a-zA-z]+):"
  inSection = False
  for i, line in enumerate(rawLines):
    line = removeComment(line.strip())
    if line == '': continue
    matchs = list(re.finditer(r"^section\s(?P<NAME>[0-9a-zA-z]+):\s{0,}", line))
    if len(matchs) != 0:
      # new section found
      sectionName = matchs[0].groups()[0]
      sections.append((sectionName, []))
      inSection = True
      continue
    if not inSection:
      raise ParseError("Expected a section declaration", i)
    sections[-1][1].append((i, line))
  return sections

def parseLine(lineNumber, line):
  name = ''
  argument = ''
  mode = 'name'
  for i,c in enumerate(line):
    if c == ' ':
      if mode == 'name':
        mode = 'argument'
      elif mode == 'argument':
        mode = 'name'
      continue
    
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
  return (lineNumber, name, argument)

def parse(lines):
  instructions = []
  for i, line in lines:
    parsedLine = parseLine(i, line)
    if parsedLine == None: continue
    instructions.append(parsedLine)
  return instructions


humanCode = open(sourceFile, 'r')
lines = humanCode.readlines()

realCode = [(0, 0)]
ih = IntelHex()
addr = 0

sectionsAddrs = []
sections = parseSections(lines)

for sectionName, sectionLines in sections:
  instructions = parse(sectionLines)
  sectionsAddrs.append(addr)
  for i, name, arg in instructions:
    if name not in instructionMap:
      print(name)
      raise InvalidInstructionError()
    name = instructionMap[name]
    ih[addr] = name
    addr += 1

    # replace section reference
    if arg.startswith('@'):
      targetSection = arg.replace('@', '')
      selection = list(filter(lambda s: s[0] == targetSection, sections))
      if len(selection) == 0:
        raise ParseError(f'Invalid section reference "{targetSection}"', i)
      arg = sectionsAddrs[sections.index(selection[0])]

    arg = int(arg) if type(arg) is int or arg.isnumeric() else 0
    ih[addr] = arg
    realCode.append((name, arg))
    addr += 1

ih.write_hex_file(outputFile)

def getNameFromOpCode(code):
  for key, value in instructionMap.items():
    if code == value:
      return key
  return None

class bcolors:
  HEADER = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  ORANGE = '\033[93m'
  RED = '\033[91m'
  GRAY = '\033[90m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

print(realCode)
print('Compiled code:')
for i in range(len(realCode)):
  if i*2 in sectionsAddrs:
    print(f"{bcolors.BLUE}-- section {sections[sectionsAddrs.index(i*2)][0]}:{bcolors.ENDC}")
  name, arg = getNameFromOpCode(realCode[i][0]), realCode[i][1]
  print(
    f"{bcolors.RED}{i:02} {bcolors.ENDC}" +
    f"0x{i*2:02x} {bcolors.GRAY}{i*2:02}{bcolors.ENDC}:       " + 
    f"0x{realCode[i][0]:02x} ({bcolors.GREEN}{name}{bcolors.ENDC}) -" +
    f"  0x{arg:02x} {arg}"
  )

# for i in range(1, 100):
#   x = '\033[' + str(i) +'m'
#   endc = '\033[0m'
#   print(f"{i} {x}W{endc}")
