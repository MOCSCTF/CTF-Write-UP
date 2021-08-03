# RTLXHA2021 - WWII Code?

- Write-Up Author: RB916120 \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:**RTL{3nigm@_1s_th3_w@y_t0_g0}**

## **Question:**
> WWII Code?

```
Thehackerscrew are back! They have encrypted their message with a more advanced type of encryption.

We have intercepted this information in this specific order: Message: dvk{3ynxc@_1h_zd3_l@b_u0_u0} M3 UKW B VII 3 2 VII 16 3 VIII 6 3 eb ch af gd ij kp mn oz …

We have also found out that they have left out 4 plugboard partners. What does this mean? Can you solve this? Flag format is RTL{flag}
Author: RJCyber
```

## Write up
the format of the cipher absolutely is enigma machine which is using by German in WII.</br>
but the chall asking for the left out 4 plugboard partners.
so,below script would brute force each plugboard combination, there will many result returned with RTL.
this writeup just for record the way to bruteforce somthing for enigma machine.


```python
from enigma.machine import EnigmaMachine
from itertools import permutations
import string
"""
dvk{3ynxc@_1h_zd3_l@b_u0_u0} M3 UKW B VII 3 2 VII 16 3 VIII 6 3 eb ch af gd ij kp mn oz ...
https://www.cryptomuseum.com/crypto/enigma/wiring.htm

have to modify the plugboard.py MAX_PAIRS = 20 in python package

"""
cipher="dvk{3ynxc@_1h_zd3_l@b_u0_u0}".upper()
pb="eb ch af gd ij kp mn oz ".upper()


all=[]
word_list=""
for i in string.ascii_uppercase:
    if i not in pb.replace(" ",""):
        word_list=word_list+i



for i in permutations(word_list,8):
    ppb=pb+i[0]+i[1]+" "+i[2]+i[3]+" "+i[4]+i[5]+" "+i[6]+i[7]

    print(ppb.upper()) 
    machine = EnigmaMachine.from_key_sheet(
    rotors='VII VII VIII',
    reflector='B',
    
    # ring setting count from 0
    ring_settings=[1,2,2],
    plugboard_settings=ppb)

    # set the init position of the ring
    machine.set_display('CPF')


    ans=""   
    for v in cipher:
        if v.isalpha():
            ans=ans+machine.process_text(v)
        else:
            ans=ans+v

    print(ans)
 
    if "RTL" in ans:
        print("Plugboard is : "+ppb)
        print("Flag: " + ans)
        all.append(ans)

        
print("\n".join(all))
```

