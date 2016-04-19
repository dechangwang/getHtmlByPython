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

		print 'handling ', self.urlid

		m = re.findall(r'<li> <b>.*:</b>.*</li>', html)

		if len(m) == 0:
			m = re.findall(r'<th class="a-span2">.*?</td>', html,re.S)
			if len(m) == 0:
				 print "no"
				
			else:
				threadLock.acquire()
				file_save = open(r'F://temp/2/'+self.urlid[:-1]+'.txt','a')
				file_save.write(self.urlid)
				title = re.findall(r'<h1 id="aiv-content-title" class="content-title js-hide-on-play">.*?<', html,re.S)
				for i in title:
					file_save.write(i+'\n')
				for i in m:
					file_save.write(i+'\n')
				file_save.close()
				threadLock.release()
				
				threadLock.acquire()
				file_save = open(r'F://temp/2/'+self.urlid[:-1]+'.txt','r')
				write = ''

				line = file_save.readline()
				write = write + 'ProductId:' + line


				while line:
					line = file_save.readline()
					if line[:3] == '<h1':
						line = file_save.readline()
						line = line.lstrip()
						write = write + 'Title:' + line
						line = file_save.readline()
						continue
					if line[:3] == '<th':
						line = file_save.readline()
						line = line.lstrip()
						write = write + line[:-1] + ':'
						line = file_save.readline()
						line = file_save.readline()
						line = file_save.readline()
						items = re.findall(r'>.*?</a>', line)
						if len(items) == 0:
							items = line.lstrip()
							write = write + items[:-1].rstrip() + '|\n'
						else:
							for i in items:
								write = write + i[1:-4].lstrip() + '|'
							write = write + '\n'
						line = file_save.readline()
						line = file_save.readline()
						continue
				file_save.close()
				threadLock.release()

				threadLock.acquire()
				file_save = open(r'F://temp/2/'+self.urlid[:-1]+'.txt','w')
				file_save.write(write)
				file_save.close()
				threadLock.release()
			
		else:
			file_save = open(r'F://temp/1/'+self.urlid[:-1]+'.txt','a')
			file_save.write(self.urlid)
			title = re.findall(r'<span id="productTitle" class="a-size-large">.*?</span>', html,re.S)
			for i in title:
					file_save.write(i+'\n')
			for i in m:
				file_save.write(i+'\n')
			file_save.close()
			file_save = open(r'F://temp/1/'+self.urlid[:-1]+'.txt','r')
			write = ''

			line = file_save.readline()
			write = write + 'ProductId:' + line


			while line:
				line = file_save.readline()
				if line[:3] == '<sp':
					items = re.findall(r'>.*?</span>', line)
					for i in items:
						write = write + 'Title:' + i[1:-7].lstrip() + '\n'
					continue
				if line[:3] == '<li':
					items = re.findall(r'<b>.*?</b>', line)
					for i in items:
						write = write + i[3:-4]
					items = re.findall(r'">.*?</a>', line)
					if len(items) == 0:
						items = re.findall(r'</b>.*?</li>', line)
						for i in items:
							write = write + i[4:-5].lstrip() + '|'
						write = write + '\n'
					else:
						for i in items:
							write = write + i[2:-4] + '|'
						write = write + '\n'
					continue

			file_save.close()
			file_save = open(r'F://temp/1/'+self.urlid[:-1]+'.txt','w')
			file_save.write(write)
			file_save.close()
		
		time.sleep(0.2)
		
	except:
		print "no"
	

	

threadLock = threading.Lock()

numThreshold = 0
thresHold = 10
while(numThreshold < 10):
	print "thresHold----------first  ---%d"%numThreshold
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
		ta = os.path.exists(r'F://temp/1/'+urlid[:-1]+'.txt')
		tb = os.path.exists(r'F://temp/2/'+urlid[:-1]+'.txt')

		if ta == False and tb == False:
			f2.write(urlid)
		else:
			f3.write(urlid)

	f1.close()
	f2.close()
	f3.close()
	
	


		
