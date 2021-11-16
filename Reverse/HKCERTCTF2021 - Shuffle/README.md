# HKCERTCTF2021 - 理性與任性之間 (Shuffle)

- Write-Up Author: Rb916120 \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:hkcert21\{s1mp13_d3shu3ff3l3_1s_s1mp13\}

## Challenge Description:

| Key | Value |
| --- | ----- |
| ID | 43 |
| Tags (Categories) | #reverse #☆☆☆☆☆ |
| Challenge release timestamp | 2021-11-12T10:00:00.000Z |
| Score | 50 |
| Total solves (Final) | 60 |
| Singer (Challenge Author) | harrier |


I heard perfect shuffle is reproducible...

Hint (Updated on 13 Nov 19:05):

- What is `.pyc`? Are there some tools for reverting pyc to some readable source (maybe back to python script)?
- Maybe you can use decompyle3 or uncompyle6 to convert to pyc back to python script?
- Next you have to revert the algorithm for flag, i.e. given the output, find the corresponding input (which is flag)
- Understanding random module should help a lot... What is `random.seed`?
- Why do this always produces same result (for same input) but not randomly differ each time? Can you make use of this to revert back to flag?
- If it generate the same "shuffling" everytime, you should be able to know how the flag shuffles, then revert the process to get the flag? 

Hint: (Update on 13 Nov 22:32)
`random.seed` will reset the randomness state when you call it, so look carefully what the original script does!

Hint: (Update on 14 Nov 4:10)
Check the python version outputted by decompyle3 / uncompyle6. Python 2 and 3 are VERY different!
Also try to decompose the code into different parts if you found it too hard to understand. Maybe give it some data to test?

### Attachments

- [shuffle_03f016d972f11c15bb25d038a2bd6bb3.zip](./shuffle_03f016d972f11c15bb25d038a2bd6bb3.zip)
## Write up  
__Reference:__  
[Random Seed](https://en.wikipedia.org/wiki/Random_seed) - A random seed (or seed state, or just seed) is a number (or vector) used to initialize a pseudorandom number generator.    
[Random.shuffle](https://docs.python.org/3/library/random.html) - Shuffle the sequence x in place.  
[uncompyle6](https://github.com/rocky/python-uncompyle6) - A native Python cross-version decompiler and fragment decompiler. The successor to decompyle, uncompyle, and uncompyle2.  

---

1. first of all the challenge provide the briefly hints to instruct the participant to solve the challenge.
   the challenge given a .pyc file which is __a compiler for Python bytecode, compiling .py code into .pyc code__  
   we can simply decompile the file with [uncompyle6](https://github.com/rocky/python-uncompyle6)
   ``` python
   ~/Desktop/hkcert21/shuffle$ uncompyle6 shuffle.pyc 
    # uncompyle6 version 3.8.0
    # Python bytecode 3.8.0 (3413)
    # Decompiled from: Python 3.8.4 (default, Jul 13 2020, 21:16:07) 
    # [GCC 9.3.0]
    # Embedded file name: shuffle.py
    # Compiled at: 2021-08-17 05:58:36
    # Size of source mod 2**32: 281 bytes
    import random
    flag = open('flag.txt').read().encode()
    random.seed(len(flag))
    output = b''
    for c in flag:
        res = list(map(int, bin(c)[2:].rjust(8, '0')))
        random.shuffle(res)
        shuffled = int(''.join(map(str, res)), 2)
        output += bytes([shuffled])
    else:
        print(output)
    # okay decompiling shuffle.pyc
   ```

2. understand the code  
   the program tack the character one by one translate binary format then turn into a list for shuffle.  
   then reverse the step and print the output. it looks short and easy, the seed is the __length of the flag which is also the length of the output__.  
   once we know the seed we can predict the coming shuffle sequence  
   ```python
    import random
    flag = open('flag.txt').read().encode()
    random.seed(len(flag))
    output = b''
    for c in flag:
        ############################################
        # translate the ASCII character into binary format
        # and padding 0 to 8 bit long
        ############################################
        res = list(map(int, bin(c)[2:].rjust(8, '0')))

        ############################################
        # shuffle the list
        ############################################
        random.shuffle(res)

        ############################################
        # turn back the list into int
        ############################################
        shuffled = int(''.join(map(str, res)), 2)
        output += bytes([shuffled])
    else:
        print(output)
   ```


3. consolidate all the thing
   - the program generate the random sequence with know seed(len(output))
   - knowing the seed can predict the following sequence
   - the bit is shuffled by this sequence  
   ``` python
    import random

    def unshuffle(cipher):
      flag=b""
      ############################################
      # generate the same sequence with the seed
      ############################################
      random.seed(len(cipher))

      for c in cipher:
          ############################################
          # order in [0,1,2,3,4,5,6,7]
          ############################################
          order=list(range(8))
          res=list(map(int, bin(c)[2:].rjust(8, '0')))
          t=[0]*8
          random.shuffle(order)

          ############################################
          # revert the flag according to the predicted order
          ############################################
          for i,ori_i in enumerate(order):
              t[ori_i]=res[i]
          flag += bytes([int(''.join(map(str, t)), 2)]) 
      print(flag)

      cipher=eval(open('output.txt').read().encode())
      unshuffle(cipher)
    ```

