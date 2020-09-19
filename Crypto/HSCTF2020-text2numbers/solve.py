message = 'eczvjcbu cz qjgimwzv ljm ecpt. qqc vfgaq fqf o 
		sdgf rqp, exfem vvuh uqlg kmh fqb goen lq jtsmz. 
		a cu kabgwuagr fwsv gqi itjg idzq ig uwnjq izka 
		cbp ngw lggqgng bjs dtoczf, ktxuj qu htt spaysd ig 
		vpg dddtnmo. htt cgg kg urspjt3owr0v3u.'
		
#Lower Case Letter table
LETTERS = 'abcdefghijklmnopqrstuvwxyz'

for key in range(len(LETTERS)):
   translated = ''
   for symbol in message:
       if symbol.strip() and symbol in LETTERS: 
           translated = translated +(LETTERS[(LETTERS.index(symbol) + key) % 26])  
       else:
           translated = translated + symbol
   print('Hacking key #%s: %s' % (key, translated))