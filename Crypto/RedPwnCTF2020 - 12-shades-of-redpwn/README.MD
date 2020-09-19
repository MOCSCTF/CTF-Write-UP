# RedpwnCTF2020 – 12-shades-of-redpwn

- Write-Up Author: Bon \[[MOCTF](https://www.facebook.com/MOCSCTF)\]

- Flag:**flag{9u3ss1n9_1s_4n_4rt}**

## **Question:**
> 12-shades-of-redpwn

```
Everyone's favorite guess god Tux just sent me a flag that he somehow encrypted with a color wheel!

I don't even know where to start, the wheel looks more like a clock than a cipher... can you help me crack the code?

Author: Boolean

Given: ciphertext.jpg && color-wheel.jpg
```

![img](./img/1.jpg)

![img](./img/2.jpg)

## Write up
>check two images and the questions, thinking of the color-wheel.jpg is sth like a clock.
and more, the first 8 color in ciphertext.jpg which should be corresponding to string 'flag'
by inspection, every color width is 500 pixel</br>first scripting for taking the RGB value in the ciphertext.jpg

```python
from PIL import Image

im=Image.open('ciphertext.jpg')
pix=im.load()
(w,h)=im.size
for i in range(int(w/500)):
  print(pix[i*500+50],600)
```

>remove the repeated value and blank area (255,255,255) we got exactly 12 color.</br>manually compare with the color-wheel.jpg, we got the following match.

```python
def clock(pix):
  switcher={
    (255, 204, 0):1,
    (255, 101, 1):2,
    (255, 51, 0):3,	
    (254, 0, 0):4 ,	
    (152, 0, 101):5,
    (153, 0, 153):6,
    (103, 0, 153):7,
    (0, 0, 254):8,	
    (0, 152, 153):9,
    (0, 153, 0):'a',
    (0, 255, 1):'b',
    (255, 255, 0):0,
	(255, 255, 255):' '
    }
  return (switcher.get(pix,"Invalid arg"))
```

>run the script again use the above matching.

```
tempflag=''
for i in range(int(w/500)):
  tempflag+=str(clock(pix[i*500+50],600))
```

>we got the flag in base12 form, transform it to base10 and we get the flag

```
for i in tempflag[1:-1].split(","):
  print(chr(int(i,12)),end="")
```

>flag is flag{9u3ss1n9_1s_4n_4rt}

