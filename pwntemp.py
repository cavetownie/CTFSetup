#!/usr/bin/env python3
from pwn import *
import ctypes

fname = "vuln"
ip = "0.0.0.0"
port = 1337

#set target binary and context
elf = context.binary = ELF(f"./{fname}")

terminalSetting = ["tmux", "new-window"]                                                                                                                                                                                                                
context.clear(terminal=terminalSetting, binary=elf)  

#set libc for pwntools
#libc = ELF("libc.so.6")

gdbscript = """
b *main
"""

mode = "debug"

if mode == "attach":
    io = process(f"./{fname}", aslr=False)
elif mode == "debug":
    io = pwnlib.gdb.debug(f"./{fname}", aslr=False, gdbscript=gdbscript)
elif mode == "remote":
    io = remote(ip, port)

# this will import the libc rand() fucntion that we can use it in your python script
# libc = ctypes.CDLL("/lib/x86_64-linux-gnu/libc.so.6")

def pwn():
    print(io.recvline())

    io.interactive()

if __name__ == "__main__":
    pwn()

# cyclic
# pattern = cyclic_gen()
# pattern = pattern.get(100)
# point = cyclic_find("aaaa", endian = "little")
# padding = b"A"*point
