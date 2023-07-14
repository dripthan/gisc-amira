
# imports
import pyperclip

# all u insts
ain = 0b1000000000000000000000
bIn = 0b0100000000000000000000
aot = 0b0010000000000000000000
bot = 0b0001000000000000000000
mai = 0b0000100000000000000000
fgi = 0b0000010000000000000000
iri = 0b0000001000000000000000
iro = 0b0000000100000000000000
pci = 0b0000000010000000000000
pco = 0b0000000001000000000000
pce = 0b0000000000100000000000
end = 0b0000000000010000000000
op3 = 0b0000000000001000000000
op2 = 0b0000000000000100000000
op1 = 0b0000000000000010000000
op0 = 0b0000000000000001000000
alu = 0b0000000000000000100000
rin = 0b0000000000000000010000
rot = 0b0000000000000000001000
inp = 0b0000000000000000000100
clr = 0b0000000000000000000010
drw = 0b0000000000000000000001

# insts
insts = [

  # nop & hlt
  [ pco | mai, rot | iri | pce ],
  [  ],

  # ldi
  [ pco | mai, rot | iri | pce, iro | ain, end ],
  [ pco | mai, rot | iri | pce, iro | bIn, end ],

  # ld
  [ pco | mai, rot | iri | pce, iro | mai, rot | ain, end ],
  [ pco | mai, rot | iri | pce, iro | mai, rot | bIn, end ],

  # sto
  [ pco | mai, rot | iri | pce, iro | mai, aot | rin, end ],
  [ pco | mai, rot | iri | pce, iro | mai, bot | rin, end ],

  # aub
  [ pco | mai, rot | iri | pce, bot | mai, rot | ain, end ],
  [ pco | mai, rot | iri | pce, bot | mai, aot | rin, end ],

  # atb
  [ pco | mai, rot | iri | pce, aot | bIn, end ],

  # inp
  [ pco | mai, rot | iri | pce, inp | ain, end ],
  [ pco | mai, rot | iri | pce, clr, end ],
  [ pco | mai, rot | iri | pce, drw, end ],

  # jmp
  [ pco | mai, rot | iri | pce, iro | pci, end ],
  [ pco | mai, rot | iri | pce ],
  [ pco | mai, rot | iri | pce ],
  [ pco | mai, rot | iri | pce ],

  # alu
  [ pco | mai, rot | iri | pce, alu | 0x0 | 0x0 | 0x0 | 0x0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, alu | 0x0 | 0x0 | 0x0 | op0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, alu | 0x0 | 0x0 | op1 | 0x0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, alu | 0x0 | 0x0 | op1 | op0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, alu | 0x0 | op2 | 0x0 | 0x0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, alu | 0x0 | op2 | 0x0 | op0 | ain, fgi, end ],

  [ pco | mai, rot | iri | pce, alu | 0x0 | op2 | op1 | 0x0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, alu | 0x0 | op2 | op1 | op0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, alu | op3 | 0x0 | 0x0 | 0x0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, alu | op3 | 0x0 | 0x0 | op0 | ain, fgi, end ],
  [ pco | mai, rot | iri | pce, fgi, end ]

]

# array to hold ucode
ucode = []

# allocate
for flag in range(0b111 + 1):
  for inst in range(0b11111 + 1):
    for step in range(0b111 + 1):
      ucode.append(hex(0))

# unconditionals
for flag in range(0b111 + 1):
  for inst in range(0b11111 + 1):
    for step in range(0b111 + 1):
      ucode_index = (flag << 8) + (inst << 3) + step
      if inst < len(insts):
        current_inst = insts[inst]
        if step < len(current_inst):
          ucode[ucode_index] = hex(current_inst[step])

# conditionals
for flag in range(0b111 + 1):
  for inst in range(0b11111 + 1):
    for step in range(0b111 + 1):
      ucode_index = (flag << 8) + (inst << 3) + step
      if inst < len(insts):
        jump_conditions = [
          inst == 0x0f and flag & 0b001 == 1,
          inst == 0x10 and flag & 0b010 == 2,
          inst == 0x11 and flag & 0b100 == 4
        ]
        current_inst = insts[inst]
        if True in jump_conditions:
          current_inst = [ pco | mai, rot | iri | pce, iro | pci, end ]
          if step < len(current_inst):
            ucode[ucode_index] = hex(current_inst[step])

# format and copy
pyperclip.copy(' '.join(ucode))
print('paste it somewhere dawg')