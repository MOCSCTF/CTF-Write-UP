# Hacktober2020 - What Lies In The shadows

- Write-Up Author: Rb916120 \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:flag{w3lcome_t0_d34df4ce}

## **Question:**
What Lies In The shadows

![img](./img/1.PNG)


## Write up
**First, below tool required in this article.**</br>
[Tor Browser](https://www.torproject.org/) -  all in one browser powered by Firefox that let you easy to surf onion network a.k.a **drak web**

**reference:**</br>
[Onion routing](https://en.wikipedia.org/wiki/Onion_routing)

the chall mentioned ghosttown is a forum, we can search in google for the result.</br>
https://www.ghosttown.xyz/


according to the [Intel page](http://ctf.cyberhacktics.com/intel). spookyboi is the recruiter person.</br>
![img](./img/2.PNG)


search spookyboi in ghost town there is only 1 relevance post.</br>
https://www.ghosttown.xyz/t/trick-or-treat-smell-my-feet/52/5</br>
![img](./img/3.PNG)


and spookyboi give a link https://pastebin.com/vbQZ7xwL that store a onion address.</br>
![img](./img/4.PNG)


launch Tor browser, and go to http://323epprcunnvtibo6no7libdxopwcaqgorho6slmpos7fimetb4zskad.onion/</br>
we will see the recruiter page</br>
![img](./img/5.PNG)


inspect the file, we could find the flag</br>
![img](./img/6.PNG)

>flag{w3lcome_t0_d34df4ce}