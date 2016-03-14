#-*- encoding: utf-8 -*-
'''
Created on 2016-3-10
@author: guoyiquan
'''
import urllib2
import urllib
import re
import time
import os
import uuid
import sys
import socket
from urllib2 import Request, urlopen, URLError, HTTPError  
reload(sys)
sys.setdefaultencoding('utf-8')
#获取二级页面url
def findUrl2(html):
    re1 = re.compile('<img.*?src="http://img1.mm131.com/pic/(.*?)/.*?jpg".*?alt="(.*?)".*?width="120.*?/>',re.S)
    url2list = re.findall(re1,html)
    #print url2lst[0],url2lst[1],url2lst[2]
    return url2list
#获取html文本
def getHtml(url):
   
    headers = {'User-Agent' : 'Chrome/30.0.1599.101','DNT': '1','Referer': 'http://www.mm131.com/' ,'Accept-Language': 'zh-CN' }
    request = urllib2.Request(url,headers = headers)
    #id = urllib.urlopen(url).code
    #print id
    html = urllib2.urlopen(request).read().decode('gbk') #解码为utf-8
    #print html
    return html
#获取图像链接
def getImage(detail):
    picpath = detail[1]
    if not os.path.exists(picpath):
        cnt = 1
        os.makedirs(picpath)
    else:
        cnt = 0   
    os.chdir(picpath)  
    path = os.getcwd()
    #print path
    for x in os.listdir(path):
        cnt += 1
    #print num 
    while(1):
        imgurl = 'http://img1.mm131.com/pic/'+detail[0]+'/'+str(cnt)+'.jpg'
        #print imgurl
        print cnt
        id = urllib.urlopen(imgurl).code
 	if(id==404):
	    break
        name = '%s.jpg' % cnt       
        target = picpath+"\\%s.jpg" % cnt
        #print "The photos location is:"+target
	if os.path.exists(name):
	    time.sleep(1)
            cnt += 1
	    print 'file exist\n'
	    continue
        download_img = urllib.urlretrieve(imgurl,'%s.jpg' % cnt)#将图片下载到指定
        time.sleep(10)
        #print(imgurl)
        cnt += 1
    path = os.getcwd()
    parent_path = os.path.dirname(path)
    #print parent_path
    os.chdir(parent_path)

if __name__ == '__main__':
    print '''            *****************************************
            **    Welcome to Spider for CHUNMEIMEI    **
            **      Created on 2016-3-10              **
            **      @author: KeepMoves                **
            *****************************************'''
    txtlog = 'Log.txt'
    fLog = open(txtlog,'a')
    pathRoot = os.getcwd()
    pageCnt = 0;
    for x in os.listdir(pathRoot):
        pageCnt += 1
    pageCnt = pageCnt - 9 
    print pageCnt
    for page in range(1,66):
        if (page == 1):
	    html = 'http://www.mm131.com/xinggan/'
	else:
            html = 'http://www.mm131.com/xinggan/list_6_'+str(page)+'.html'
        if(page<pageCnt):
            page += 1
            continue
        os.chdir('/home/keepmoves/MM')
        path = os.getcwd()
        #print path
        picpath = 'sexPage'+str(page)
        if not os.path.exists(picpath):
            cnt = 1
            os.makedirs(picpath)
        else:
            cnt = 0   
        os.chdir(picpath)
        pagePath = os.getcwd()
        numInPages = 0
        for x in os.listdir(pagePath):
            numInPages += 1  
        #print html
        fLog.write(html)
        fLog.write('\n')
        fLog.write(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
        fLog.write('\n')
        html = getHtml(html)
        detllst = findUrl2(html)
        numInPage = 1
        for detail in detllst:
            if(numInPage < numInPages):
                numInPage += 1
                continue
            pos = 'Page:\t' +str(page)+'/65'+ '\tNo:\t' + str(numInPage)+'/20'
            print pos
            print detail[1]
            fLog.write(str(numInPage))
            fLog.write(detail[1])
            numInPage += 1
            fLog.write('\n')
            #print detail[0],detail[1]
	    imageList = getImage(detail)
    print "Finished."

