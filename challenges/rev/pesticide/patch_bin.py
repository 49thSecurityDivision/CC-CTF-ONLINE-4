#!/dev/null 

from capstone import *

with open("do_not_upload", "rb") as file:
    code = file.read()

md = Cs(CS_ARCH_X86, CS_MODE_64)
for i in md.disasm(code, 0x1060):
    print(f"i: {i.mnemonic} {i.op_str}");
