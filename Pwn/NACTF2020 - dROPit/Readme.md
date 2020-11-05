# NACTF2020 - dROPit

- Write-Up Author: Rb916120 \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:nactf{r0p_y0ur_w4y_t0_v1ct0ry_698jB84iO4OH1cUe}

## **Question:**
dROPit - 300

>You're on your own this time. Can you get a shell?  
>nc challenges.ctfd.io 30261  
>-asphyxia  
>  
>Hint  
>https://libc.rip

[dROPit](./dROPit)

## Write up
**below tools mentioned in this writeup.**  
[libc-database](https://github.com/niklasb/libc-database) - search for libc with 12bits offset,super useful when you don't know the libc file  

**Reference:**  
[Stack frame layout on x86-64](https://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64)  
[PLT and GOT](https://www.technovelty.org/linux/plt-and-got-the-key-to-code-sharing-and-dynamic-libraries.html)
[ELF document](https://stevens.netmeister.org/631/elf.html)

---

in Pwn challange, the first thing we do is check the security properties of the executable file.
```
$checksec dropit
[*] '/root/Desktop/NACTF/dropit'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)


```

ok there is only RELRO and NX enabled. at least we don't have to deal with PIE...  

```
Relocation Read-Only (RELRO)
Relocation Read-Only (or RELRO) is a security measure which makes some binary sections read-only.

Stack Canaries
Stack Canaries are a secret value placed on the stack which changes every time the program is started. 
Prior to a function return, the stack canary is checked and if it appears to be modified, the program exits immeadiately.

No eXecute (NX Bit)
The No eXecute or the NX bit (also known as Data Execution Prevention or DEP) marks certain areas of the program as not executable, 
meaning that stored input or data cannot be executed as code. This is significant because it prevents attackers from being able to jump to custom shellcode that they've stored on the stack or in a global variable.

Position Independent Executables (PIE)
PIE is a body of machine code that, being placed somewhere in the primary memory, executes properly regardless of its absolute address

```

reversed the executable file and there is a simple program to get the input with **fgets**. 
```c
undefined8 main(void)

{
  char local_38 [48];
  
  setvbuf(stdout,(char *)0x0,2,0);
  puts("?");
  fgets(local_38,100,stdin);
  return 0;
}

```

look at the man page of **fgets** , fgets() only reconigze null byte ('\0') as terminate character.  
which mean we can overflow the stack with this function.  
```shell
FGETC(3)                                 Linux Programmer's Manual                                 FGETC(3)

NAME
       fgetc, fgets, getc, getchar, ungetc - input of characters and strings

SYNOPSIS
       #include <stdio.h>

       int fgetc(FILE *stream);

       char *fgets(char *s, int size, FILE *stream);

       int getc(FILE *stream);

       int getchar(void);

       int ungetc(int c, FILE *stream);

DESCRIPTION
......

       fgets()  reads  in at most one less than size characters from stream and stores them into the buffer
       pointed to by s.  Reading stops after an EOF or a newline.  If a newline is read, it is stored  into
       the buffer.  A terminating null byte ('\0') is stored after the last character in the buffer.

......

```


