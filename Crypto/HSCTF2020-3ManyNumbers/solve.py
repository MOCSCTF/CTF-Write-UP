for i in message:
    message1.append(int(i/1000)*27+ int((i%1000)/100)*9 + int((i%100)/10)*3 + int((i%10)))

letter = "abcdefghijklmnopqrstuvwxyz _"
	
message = [	22,12,200,12,1000,212,12,1000,210,201,
			12,1000,202,12,200,112,1,200,221,1000,202,
			120,1000,21,12,202,1000,202,22,12,1000,20,
			110,1,21,1000,202,22,200,12,12,1001,11,100,
			21,100,202,201,1001,100,201,112,202,1001,211,
			12,200,221,1001,201,12,10,210,200,12]
			
message1=[]
translated=""

for i in message:
    message1.append(int(i/1000)*27+ int((i%1000)/100)*9 + int((i%100)/10)*3 + int((i%10)))
	
for j in message1:
    translated=translated+letter[j-1]
	
print (translated)