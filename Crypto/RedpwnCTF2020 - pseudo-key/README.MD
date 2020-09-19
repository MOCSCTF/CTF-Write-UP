# RedpwnCTF2020 – pseudo-key

- Write-Up Author: Bon \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:**flag{i_guess_pseudo_keys_are_pseudo_secure}**

## **Question:**
> pseudo-key

```
Keys are not always as they seem...
Note: Make sure to wrap the plaintext with flag{} before you submit!
```

[pseudo-key.py](./pseudo-key.py)

[pseudo-key-output.txt](./pseudo-key-output.txt)
## Write up
>check pseudo-key.py, find out the encryption is just simply use the sum of flag and key then mod 26.

```python
#!/usr/bin/env python3

from string import ascii_lowercase

chr_to_num = {c: i for i, c in enumerate(ascii_lowercase)}
num_to_chr = {i: c for i, c in enumerate(ascii_lowercase)}

def encrypt(ptxt, key):
    ptxt = ptxt.lower()
    key = ''.join(key[i % len(key)] for i in range(len(ptxt))).lower()
    ctxt = ''
    for i in range(len(ptxt)):
        if ptxt[i] == '_':
            ctxt += '_'
            continue
        x = chr_to_num[ptxt[i]]
        y = chr_to_num[key[i]]
        ctxt += num_to_chr[(x + y) % 26] <-- here!!
    return ctxt

with open('flag.txt') as f, open('key.txt') as k:
    flag = f.read()
    key = k.read()

ptxt = flag[5:-1]

ctxt = encrypt(ptxt,key)
pseudo_key = encrypt(key,key)

print('Ciphertext:',ctxt)
print('Pseudo-key:',pseudo_key)
```

>check the pseudo-key-output.txt which provides the encrypted key and the cipher.

```
Ciphertext: z_jjaoo_rljlhr_gauf_twv_shaqzb_ljtyut
Pseudo-key: iigesssaemk
```

>use the following script to decrypt the key:

```python
def dkey(key):
    ptxt = ''
    for i in range(len(key)):
        x = chr_to_num[key[i]]
        ptxt +=num_to_chr[(x+26)/2]
    return ptxt
```

>because of the encrypt function mod the cipher to 26, so we have two list of keys in combination for the real key.

```
key1:'rrqpwwwnpts'
key2:'eedcjjjacgf'
```

>use two keys in the decrypt script for decrypt the cipher:

```python
def decrypt(cipher, key):
    cipher = cipher.lower()
    key = ''.join(key[i % len(key)] for i in range(len(cipher))).lower()
    ptxt = ''
    for i in range(len(cipher)):
        if cipher[i] == '_':
            ptxt += '_'
            continue
        y = chr_to_num[cipher[i]]
        x = chr_to_num[key[i]]
        if x>y:
            ptxt +=num_to_chr[y+26-x]
        else:
            ptxt +=num_to_chr[y-x]
    return ptxt
```

>turns out two result:

```
'i_tuess_csruqb_keys_aee_cseudo_srchee'
'v_ghrff_pfehdo_xrlf_nrr_pfrhqb_fepurr'
```

>just by inspecting, the result is 'i_guess_pseudo_keys_are_pseudo_secure' by using the key 'redpwwwnctf'
flag is flag{i_guess_pseudo_keys_are_pseudo_secure}
