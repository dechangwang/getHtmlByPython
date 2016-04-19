import os

f = open('F://temp/part0.txt','r')

f2 = open('F://temp/norun2.txt','a')

urlid = f.readline()

while urlid:
	urlid = f.readline()
	ta = os.path.exists(r'F://temp/3/'+urlid[:-1]+'.txt')
	if ta == False:
		f2.write(urlid)
	
		

print "finished"
