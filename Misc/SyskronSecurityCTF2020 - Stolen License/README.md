# Syskron Security CTF 2020 - Stolen License
- Write-Up Author: Bon \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag: 78124512846934984669

## **Question:**
Stolen License

>Challenge description
>We found another file on the dark net! It seems that cyber criminals stole some of our license keys and put them up for sale. We tracked down a ZIP file at [link removed as it is unavailable now] (password for download syskron.CTF2020).
We don't know the password of the ZIP file, but maybe it is weak encryption that can be easily cracked. If you find any valid license key, let us know.

Flag format: license-key (e.g., 7812…110).

Be aware: We need skilled people! If you send us random numbers, we will assign another security contractor.

Attachment: [licenses.zip](https://drive.google.com/file/d/1-ZuMn02TUOxTW_6EBvEjTRqQOxgaEA7K/view?usp=sharing)

## **Hint:**
>Hint 1
Another security contractor told us that the password of the ZIP file may be a single word that was recently added to a well-known dictionary.

>Hint 2
We already told you how we create our check digits …

>Hint 3
A security team pinpointed the possible words to open the ZIP file to https://www.merriam-webster.com/words-at-play/new-words-in-the-dictionary

## Write up
This challenge quite challenging that we can’t figure out the password of given zip file until we unlock the hint 3.

>Found the password of the zip file is **nosocomephobia**.

Then I got 1000 PNGs of license documents, how can we find the valid license key?

Hint 2 leads a great direction, we known the ‘Check Digit’ challenge gives the answer (**Luhn algorithm**)

What I need to do is to grap 1000 license keys from those PNGs and check the one that can pass Luhn algorithm. 

![img](./img/1.png) 

>The flag is 78124512846934984669 