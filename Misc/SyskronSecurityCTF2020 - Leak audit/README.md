# Syskron Security CTF 2020 - Leak audit
- Write-Up Author: Bon \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag: 376_mah6geiVoo_21

## **Question:**
Leak audit

>Challenge description
>We found an old dump of our employee database on the dark net! Please check the database and send us the requested information:
1.	How many employee records are in the file?
2.	Are there any employees that use the same password? (If true, send us the password for further investigation.)
3.	In 2017, we switched to bcrypt to securely store the passwords. How many records are protected with bcrypt?

Flag format: answer1_answer2_answer3 (e.g., 1000_passw0rd_987).

Attachment: [BB-inDu57rY-P0W3R-L34k3r2.tar.gz](./BB-inDu57rY-P0W3R-L34k3r2.tar.gz)

## Write up
This challenge is very straight forward. To test SQL skills.
First question:
```
SELECT count(*) 
FROM personal;
```
>Given **376**

Second question:
```
SELECT count(password) as ct ,password
FROM personal
Group by password 
ORDER BY ct DESC  
```

>Given **mah6geiVoo** as its count is 2

Thrid question:
```
SELECT count(password)
FROM personal
WHERE password like '%2b%'
```

>Given **21**

>So the flag is 376_mah6geiVoo_21