message = 'fvbl}bf334'
translated = ''
#translated variable is used to contain the correct input.

for symbol in message:
   translated = translated + chr(ord(symbol)-3)
   
print('Hacking key: %s' % (translated))