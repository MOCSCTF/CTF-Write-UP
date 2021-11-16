import random

def unshuffle(cipher,flag_len):
    flag=b""
    random.seed(len(cipher))
    for c in cipher:
        order=list(range(8))
        res=list(map(int, bin(c)[2:].rjust(8, '0')))
        t=[0]*8
        random.shuffle(order)
        for i,ori_i in enumerate(order):
            t[ori_i]=res[i]
        flag += bytes([int(''.join(map(str, t)), 2)]) 
    print(flag)

cipher=eval(open('output.txt').read().encode())
unshuffle(cipher,len(cipher))