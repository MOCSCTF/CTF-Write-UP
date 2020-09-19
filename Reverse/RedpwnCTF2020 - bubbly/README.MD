# RedpwnCTF2020 – bubbly

- Write-Up Author: Bon \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:**flag{4ft3r_y0u_put_u54c0_0n_y0ur_c011ege_4pp5_y0u_5t1ll_h4ve_t0_d0_th15_57uff}**

## **Question:**
> bubbly

```
Author: roerohan

A possible way to solve this challenge is decompiling the binary and trying to understand what's happening in the code.
```
[bubbly](./bubbly)

## Write up
>put the file in ida and review the code, found out there is a hardcode array need to sorted to get flag.
![img](./img/1png)

```c
  while( true ) {
    __isoc99_scanf(&DAT_00102058);
    if (8 < i) break;
    nums[i] = nums[i] ^ nums[i + 1];
    nums[i + 1] = nums[i + 1] ^ nums[i];
    nums[i] = nums[i] ^ nums[i + 1];
    pass = check();
  }
```
>while input a integer less than 9, the program will swap the corresponding position number over the behind one.</br>so we can sort it by input the following numbers.
```
2
1
2
7
6
5
4
3
4
8
7
6
5
8
7
6
8
7
8
9 <-- which end the sort function
```

>then we get the flag.</br>flag is  flag{4ft3r_y0u_put_u54c0_0n_y0ur_c011ege_4pp5_y0u_5t1ll_h4ve_t0_d0_th15_57uff}
