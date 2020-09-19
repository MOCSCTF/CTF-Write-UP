# RedpwnCTF2020 - itsy-bitsy

- Write-Up Author: Bon \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:**Flag{bits_leaking_out_down_the_water_spout}**

## **Question:**
> itsy-bitsy

```
The itsy-bitsy spider climbed up the water spout...
nc 2020.redpwnc.tf 31284
itsy-bitsy.py
```

[itsy-bitsy.py](./itsy-bitsy.py)

## Write up
>from the script we know the cipher is encrypted by generating random number define by input the lower bound and upper bound number.
for example, if I send i=1,j=2, the data range will be from 10 or 11, if i send i=3 & j=4 so the data range will be from 1000 to 1111.
so if i loop all prime numbers until the length of cipher it will show the flag.</br>and the operation for the key and the cipher, since the encryption method is using xor, so if the cipher bit is 0 and key bit is 1, the result will be 1.

```python
def spec(bit_str_1, bit_str_2):
    xor_res = ''
    for i in range(len(bit_str_1)):
        bit_1 = bit_str_1[i]
        bit_2 = bit_str_2[i]
        if bit_1=='0' and bit_2=='1':
          xor_res += '1'
        else:
          xor_res+='0'
    return xor_res
```

>put all result bit by bit using or to get flag

```
def bor(bit_str_1, bit_str_2):
    xor_res = ''
    for i in range(len(bit_str_1)):
        bit_1 = bit_str_1[i]
        bit_2 = bit_str_2[i]
        xor_res += str(int(bit_1) or int(bit_2))
    return xor_res

ansbit=301
ans='0'*ansbit
final_ans=''
j=0

for i in range(ansbit):
  if isPrime(i):
    conn =remote("2020.redpwnc.tf",31284)
    conn.recvuntil("Enter an integer i such that i > 0:")
    conn.sendline(str(i-1))
    conn.recvuntil("Enter an integer j such that j > i > 0:")
    conn.sendline(str(i))
    conn.recvuntil("Ciphertext: ")
    temp_c=conn.recv()
    conn.close()
    ans=bor(ans,spec(temp_c,(('1'+'0'*(i-1))*(ansbit//i+1))[0:ansbit]))


for j in range(0,len(ans),7):
    final_ans+=chr(int('0'+ans[j:j+7],2))
```

>flag is Flag{bits_leaking_out_down_the_water_spout}
