# PICOCTF2019 - Logon

- Write-Up Author: Teru Lei \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:**picoCTF{th3_c0nsp1r4cy_l1v3s_2e19dad3}**
## **Question:**
>Logon

![img](./img/1.png)

## Write up:

>Open the web page:
![img](./img/2.png)

>The question mentioned that “login as logon”, so the username should be “logon”. First step try to observe the source code, no special.
![img](./img/3.png)

>Then try to login with user “logon” and try some simple password (e.g. password”) to observe the reaction of the webpage:
![img](./img/4.png)

>It’s login anyway but no flag. Observe the source code again, same no special was found:
![img](./img/5.png)

>Next step we may try to observe the request and response of the web link, and if necessary, modify the web request or reply. BurpSuite community edition is one of the most popular tool to do this task. BurpSuite community edition come with Kali Linux already. Open BurpSuite, select “Temporary Project”, then click “Next”.
![img](./img/6.png)

>Keep “Use Burp defaults”, then click “Start Burp”
![img](./img/7.png)

>Click “Proxy” tab, make sure “Intercept is on”:
![img](./img/8.png)

>Open the browser of your machine, point your browser proxy IP to 127.0.0.1, port 8080, so that the browser outgoing traffic will be intercepted by BurpSuite:
![img](./img/9.png)

>Browse the web page, BurpSuite will intercept the traffic:
![img](./img/10.png)
 
>Observe the cookie, there is “admin=False”, it’s interesting, possibly the flag needs to be achieved by admin. So we can try to change the cookie to “admin=True”. In order to clearly observe the response from web server, we can highlight the raw web request in BurpSuite, right click then choose to intercept the response of the request, then press “Forward”:
![img](./img/11.png)

>We can observe there is redirection from web server:
![img](./img/12.png)

>The response will set back “admin=False”, try to set back to “admin=True” again but still cannot get the flag:
![img](./img/13.png)

>There is hint in the question:
![img](./img/14.png)

>With the hint, we can try to remove the password part in the cookie, try again, then we can get the flag:
![img](./img/15.png)





