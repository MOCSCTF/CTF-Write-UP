# Syskron Security CTF 2020 - Firmware update
- Write-Up Author: Bon \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag: syskronCTF{s3Cur3_uPd4T3}

## **Question:**
Firmware update

>Challenge description
>The crypto software LibrePLC at BB Industry is continuously receiving updates. Unfortunately, the responsible employee left the company a few weeks ago and hasn't deployed the most recent firmware with important security updates. He just left a note with 5157CA3SDGF463249FBF.

We urgently need the new firmware!

Attachment: [LibrePLC_firmware_pack.zip](./LibrePLC_firmware_pack.zip)

## Write up
Given three zip files that are protected by password.

Since the description gives a strange note, tried on every zip file and found that one of the zip file can be unzipped.

From the above zip file, I got a file call ‘key’ and a firmware like file.
Checking the ‘key’ file found that it is a python script.

```
#!/usr/bin python3
import hashlib #line:3
import sys #line:4
def check ():
        if len (sys .argv )==1 :#
                print ("No key for you")#
                sys .exit (0 )#line:9
        else :#line:10
                OOO0OOOOOO00000OO =sys .argv [1 ]#
                return OOO0OOOOOO00000OO #line:12
def get_it (OOO0OOOOO00000OOO ):#line:14
        with open (OOO0OOOOO00000OOO ,"rb")as O0000O000O00O0000 :#line:15
                O0O0O0OOO000OOO0O =O0000O000O00O0000 .read ()
                OO0O000O0OO000O0O =hashlib .sha256 (O0O0O0OOO000OOO0O ).hexdigest ()
        return OO0O000O0OO000O0O #line:18
def keys (OOOOOOOO00OOOOOOO ):#line:20
        O0OO00OOO00OOOOOO =OOOOOOOO00OOOOOOO [::-1 ][:10 ]#line:21
        O00O00O0O0O0O0000 =OOOOOOOO00OOOOOOO [5 :20 ][::-1 ]#line:22
        O00O00O0O0O0O0000 =O0OO00OOO00OOOOOO .replace ("1","0")[::-1 ].replace ("9","sys")#
        O0OO00OOO00OOOOOO =O00O00O0O0O0O0000 .replace ("a","k").replace ("4","q").replace ("b","c").replace ("5","kron")#line:24
        O0O000OO0000O000O =OOOOOOOO00OOOOOOO [23 :50 ][::-1 ].replace ("8","n")
        O0OO0OO0OOOOO0OO0 =OOOOOOOO00OOOOOOO [50 :61 ][::-1 ].replace ("7","ctf")#
        O0OO00O00000O00O0 =(O00O00O0O0O0O0000 +O0OO0OO0OOOOO0OO0 +O0OO00OOO00OOOOOO +O0O000OO0000O000O ).upper ()#
        return O0OO00O00000O00O0 #line:30
print (keys (get_it (check ())))
```

O.O I though I gonna skip this challenge once, tried not to focus on those Os and 0s, the check function seems that need to have input for running the script.

And the get_it function seems tried to hash something use sha256. Just by curious that use the firmware file as the input and run the python script, I got **7SYSCC3076BDCTF13CC9CTFA6CB7SYSCC3076CD56579549EC5AB533EN03AFC1F9N**

Something like the unknown text given by description. Try to unzip the second zip file using the above text as password and it worked~

The second zip file gives a firmware file only, use it as the input to run and run the script, I got **CSYS0BBA60E46ABB19C5BC0CSYS0CCK60EQ1NC41E2C5DDA4C5C7D45E096162**

Finally I got the final firmware using the about text as password. Now what?

Put it into hex editor and found the key at the file header.

>syskronCTF{s3Cur3_uPd4T3}


