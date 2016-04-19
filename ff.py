import urllib2
import urllib
import cookielib
import time
import re
import threading
import os

class myThread (threading.Thread):
    def __init__(self,url,urlid):
	threading.Thread.__init__(self)
	self.url = url
	self.urlid = urlid
    def run(self):
	try:
		cj = cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		urllib2.install_opener(opener)

		req = urllib2.Request(self.url)
		operate = opener.open(req)
		html = operate.read()

		print r'handling ', self.urlid

		m = re.findall(r'>.*?</a></b></span>', html)

		if len(m) != 0:
			
			file_save = open(r'F://temp/3/'+self.urlid[:-1]+'.txt','a')

			file_save.write('ProductId:' + self.urlid)
			for i in m:
				j = i[1:-15].split('>')
				file_save.write(j[-1]+'\n')
			file_save.close()
		
		time.sleep(0.2)
		
	except:
		print "no"
	

	

threadLock = threading.Lock()

numThreshold = 0
thresHold = 10
while(numThreshold < 100):
    print "thresHold----------firen  ---%d"%numThreshold
    threads = []
    f = open('F://temp/part%d.txt'%numThreshold,'r')
    urlid = f.readline()
    url = 'http://www.amazon.com/dp/' + urlid
    num = 100
    i = 0
    while(i < num):
	    threads.append(myThread(url,urlid))
	    i +=1
	    if (i>=num):
		    break
	    urlid = f.readline()
	    url = 'http://www.amazon.com/dp/' + urlid
    j = 0
    while(j<num):
	    threads[j].start()
	    j += 1
	    
    count = 0
    urlid = f.readline()
    url = 'http://www.amazon.com/dp/' + urlid
    while urlid:
	j = 0
	while(j<num):
	    if(threads[j].is_alive()):
		j += 1
	    else:
		count = count + 1
		print count / 136082.0 * 100, '%'
		urlid = f.readline()
		url = 'http://www.amazon.com/dp/' + urlid
		if urlid:
		    threads[j] = myThread(url,urlid)
		    threads[j].start()
		    j += 1
		else:
		    break
    f.close()
    time.sleep(10)



    f1 = open('F://temp/part%d.txt'%numThreshold,'r')
    global numThreshold
    numThreshold +=1
    print "thresHold----------%d"%numThreshold
    f2 = open('F://temp/part%d.txt'%numThreshold,'a')
    f3 = open('F://temp/yes.txt','a')

    urlid = f1.readline()

    while urlid:
	    urlid = f1.readline()
	    ta = os.path.exists(r'F://temp/3/'+urlid[:-1]+'.txt')

	    if ta == False:
		    f2.write(urlid)
	    else:
		    f3.write(urlid)

    f1.close()
    f2.close()
    f3.close()
	
	


		
