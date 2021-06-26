from pwn import *
import time
s = ''
r = remote('not-really-math.hsc.tf', 1337)
r.recvuntil('== proof-of-work: disabled ==\n')
for i in range(0,200):
    sep2=1
    x=r.recvline()
    print(x)
    if (': ' in x):
        x=x[2:]
    time.sleep(1) 
    if ('flag' in x) or ('Unfortunately' in x):
        break    
    sep1=x.split('m')
    print(sep1)
    for y in sep1:
        m=y.split('a')
        m = [int(k) for k in m]
        n=sum(m)
        sep2=sep2*n   
    r.sendline(str(sep2%(2**32-1)))

print(x)
	
