
# imports
import sys
import pyperclip

# all insts
insts = [
  'nop',
  'hlt',
  'ldia',
  'ldib',
  'lda',
  'ldb',
  'sta',
  'stb',
  'ldaub',
  'staub',
  'atb',
  'inp',
  'clr',
  'drw',
  'jmp',
  'jc',
  'jz',
  'jeq',
  'add',
  'sub',
  'mul',
  'div',
  'shl',
  'shr',
  'not',
  'and',
  'or',
  'xor',
  'cmp'
]

# variables to keep things neat
lines = []
assem = []
jumps = {}

# get lines that we care about from file
with open(sys.argv[1]) as f:
  lines = f.readlines()
  lines = list(filter(lambda line: len(line.split()) > 0, lines))
  lines = list(filter(lambda line: line.split()[0] != ';', lines))

# set the assem code to all zeros
for i, v in enumerate(lines):
  assem.append(hex(0))

# deal with jump markers
for i, v in enumerate(lines):
  tokens = v.split()
  inst = tokens[0]
  if inst[-1] == ':':
    jumps[inst[0:-1]] = i

# deal with insts
for i, v in enumerate(lines):
  tokens = v.split()
  inst = tokens[0]
  if inst[-1] == ':':
    continue

  # deal with no param insts
  if len(tokens) == 1:
    inst_index = insts.index(inst)
    assem[i] = hex(inst_index << 11)
    continue

  # deal with jumps
  if inst in ['jmp', 'jc', 'jz', 'jeq']:
    inst_index = insts.index(inst)
    param = jumps[tokens[1]]
    assem[i] = hex((inst_index << 11) + param)
    continue

  # deal with others
  inst_index = insts.index(inst)
  param = int(tokens[1], base=16)
  assem[i] = hex((inst_index << 11) + param)

pyperclip.copy(' '.join(assem))
print(' '.join(assem))
print('paste it somewhere dawg')