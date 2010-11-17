#!/usr/bin/env python
#
#       pinp.py
#       
#       Copyright 2009 Marce Elizeche <marce@elendil>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import sys
import urllib, urllib2, socket
import string
import math
import time

global info,t0



def stripping(xml): #Parsea el xml
	#print xml
	socket.setdefaulttimeout(15)
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	req = urllib2.Request(xml, None, headers)
	f =	urllib2.urlopen(req)
	f = f.read()
	
	#print f
	path = f.split('path=\"')[1].split('\"')[0]
	artist = f.split('artist=\"')[1].split('\"')[0]
	title = f.split('title=\"')[1].split('\"')[0]
	return path,artist,title

def rape(url):# "Viola a Goear
    id = url.split("listen/")[1].split('/')[0]
    #idcode = id[0]
    xml = 'http://www.goear.com/tracker758.php?f='+id
    #print xml
    return xml
    

def goHunt(st):
    ids=[]
    idinfo=[]
    #print type(st)
    url = 'http://www.goear.com/search.php?q=' + urllib.quote(st)
    #print url
    #Aca hay que capturar una excepcion
    
    f = urllib.urlopen(url)
    s = f.read()
    f = f.read()
    a = s.split('<a title')
    #print a[3]
    a.pop(0)
    urls = []
    names = []
    if len(a)==1:
        return 0
    for x in a:
		#print x.split('href=\"')[1].split('\"')[0]
		#print x.split('href=\"')[1].split('\">')[1].split('<')[0]
		#sys.exit()
		urls.append((x.split('href=\"')[1].split('\"')[0]))
		names.append((x.split('href=\"')[1].split('\">')[1].split('<')[0]))

    c=0
    
    for i in urls:
        f = i.split("listen/")
        c= c+1
        id = f[1].split('/')[0]
        #idcode = id[0]
        #ids.append((c,i,names[c-1],id,idcode))
        ids.append((c,i,names[c-1],id))
    
    return ids

def godownstairs(info):
#	print info
	#global info
	arch = info[1] + " - " + info[2] + ".mp3"
	urllib.urlretrieve(info[0], arch, reporthook=dlProgress)

def format_bytes(bytes):
		if bytes is None:
			return 'N/A'
		if bytes == 0:
			exponent = 0
		else:
			exponent = long(math.log(float(bytes), 1024.0))
			suffix = 'bkMGTPEZY'[exponent]
			converted = float(bytes) / float(1024**exponent)
			return '%.2f%s' % (converted, suffix)

def calc_speed(start, now, bytes):
	dif = now - start
	if bytes == 0 or dif < 0.001: # One millisecond
		return '%10s' % '---b/s'
	return '%10s' % ('%s/s' % format_bytes(float(bytes) / dif))


def dlProgress(count, blockSize, totalSize):
	global t0
	if t0==0:
		t0=time.time()
	percent = int(count*blockSize*100/totalSize)
	#tam=format_bytes(count*blockSize)
	sys.stdout.write("\r" + info[1] + " - " + info[2] + ".mp3" + "\t%d%% \t%s" % (percent, calc_speed(t0,time.time(),count*blockSize)))
	sys.stdout.flush()

def main():
    global info,t0
    
    t0=0
    print "PINP v0.5.2\nby Marcelo Elizeche Lando\nLicensed under GPLv3\n"
    st=''
    if len(sys.argv)>1:
        for i in sys.argv:
            if i!=sys.argv[0]:
                st = st+i+'+'
        print "Buscando: " + st + "\n"
    else:
        st = raw_input("Ingresa tu Busqueda(Artista, Tema, etc): ")
        st = st.replace(" ","+")
    index = goHunt(st)
    if not index:
        print "\nNo Se encontraron Resultados..."
        return 0
    for i in range(len(index)):
        print str(index[i][0]) + ".\t" + str(index[i][2])
    num = 11
    while num>len(index):
        num = raw_input("\nIngresa el Numero de la Musica que queres bajar: ")
        if num=='':
            num='11'
        num = int(num)
        if num>len(index) or num<1:
            print "\nYo no veo ese numero ahi..."
            num=11
    xml = rape(index[num-1][1])
    info = stripping(xml)
    godownstairs(info)
    print "\nSe Termino de Descargar!\n"
    raw_input("")
    return 0
	
	
if __name__ == '__main__': main()


