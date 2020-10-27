# Syskron Security CTF 2020 - Bash history
- Write-Up Author: Bon \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag: syskronCTF{tHey-st0le-all-Data!!}

## **Question:**
Bash history

>Challenge description
>We suspect that one of BB's internal hosts has been compromised. I copied its ~./bash_history file. Maybe, there are some suspicious commands?

Attachment: [bash_history](./bash_history)

## Write up
Open the given file which is plain text of command history.

By observe that there’s some command encoded by base64 and two of them is different from others.

```
echo xYTjBNR3hsTFdGc2JDMUVZWFJoSVNGOQ==
echo ZWNobyBjM2x6YTNKdmJrTlVSbnQwU0dWNU
```

The first one shows unknown hex, just skipped it first.

The second one shows Incorrect padding error while decoding, seems that something is missing.

Since the first one has end padding, just tried to put it behind the second one and it works.

```
echo c3lza3JvbkNURnt0SGV5LXN0MGxlLWFsbC1EYXRhISF9
```

Another base64, decode it and we found the flag.
>syskronCTF{tHey-st0le-all-Data!!}
