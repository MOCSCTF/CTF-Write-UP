# Syskron Security CTF 2020 - Contact Card
- Write-Up Author: Teru Lei \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:syskronCTF{n3v3r_c11ck_unkn0wn_11nk5}

## **Question:**
Contact Card

>Challenge description  
>Some of our employees have received an email with this attachment. The message says that there was some confidential contact data leaked (Password for attachment: edeb142). We recon it is some kind of phishing, but the contact files look clean, do they?
>Info: This challenge does NOT contain any malicious files.

## Write up
>In this challenge, we are given a zip file, after unzip the file, the file structure is as below:
![img](./img/1.PNG)

>There are some contact files, and some other files are found in the folders:
>http folder (There are some cpl files, which are for Control Panel in Windows: [here](https://support.microsoft.com/en-us/help/149648/description-of-control-panel-cpl-files) Seems interesting, we can investigate further later) :
![img](./img/2.PNG) 

>https folder (All files have zero file size, seems not interesting ones):
![img](./img/3.PNG)

>Other folders are empty. According to what we have now, let’s focus on the cpl files in http folder to see if there are other clues found.

>In Kali Linux,using ‘file’ command to examine the file type, ‘string’ command to check the strings found in the file, ‘exiftool’ to inspect metadata, and use ‘binwalk’ to check if there is hidden file. We can see that all those cpl files are binary zero, except **www.random4.cpl** (In binwalk, there is hidden file found but from ‘algorithm’ and further checked the binary, it’s caused by incorrect recognition of magic bytes of binwalk, there is no hidden file): 
![img](./img/4.PNG)
![img](./img/5.PNG)
![img](./img/6.PNG)

>And from the contact card file, we can see the contact card for ‘Maximilian Baecker’, the Website field is **http.\\www.random4.cpl** (In real world, you should not open the suspected file outside a controlled environment):
![img](./img/7.PNG)

>At this stage, we can suspect that the file **www.random4.cpl** is malware. With some further googling, we can find a vulnerability related to this scenario [here](http://hyp3rlinx.altervista.org/advisories/MICROSOFT-WINDOWS-VCF-FILE-INSUFFICIENT-WARNING-REMOTE-CODE-EXECUTION.txt):
```
[Security Issue]
This vulnerability allows remote attackers to execute arbitrary code on vulnerable installations of Microsoft Windows.
User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the processing of VCard files. Crafted data in a VCard file can cause Windows to display a dangerous hyperlink.
The user interface fails to provide any indication of the hazard.

An attacker can leverage this vulnerability to execute code in the context of the current user.
```

>To further study the behavior of **www.random4.cpl**, we can try to do some static analysis, for example, ghidra to try to decompile the binary. Actually, a message box is prompted when the cpl file is executed:
![img](./img/8.PNG)

>Or, we can simply upload the cpl file to some online malware analysis website (e.g. hybrid-analysis.com) to analysis. We can also see a message box is prompted when the binary is run in sandbox:
![img](./img/9.PNG)

>Further examine the content of message box, there is string ‘xSAvEyND’ and it mentioned that ‘We pasted this for you’. Recalled another 300 marks challenge ‘HID’, pastebin.com is used for the hacker to download malicious powershell, and the length of ‘xSAvEyND’ is the same as the path section of pastebin.com, so it’s possible that same technique is used here. let’s try to access **https://pastebin.com/raw/xSAvEyND**:
![img](./img/9.PNG)

>syskronCTF{n3v3r_c11ck_unkn0wn_11nk5}


