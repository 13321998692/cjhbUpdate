#coding=utf-8
from progress.bar import Bar
import os
import re
maxi=0
def IDMdownload(DownUrl, DownPath, FileName):
    IDMPath = "C:\\Program Files (x86)\\Internet Download Manager\\"
    os.chdir(IDMPath)
    IDM = "IDMan.exe"
    command = ' '.join([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/a'])
    os.system(command)
bar = Bar('Processing', max=13000,
          suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')
full=0
mdir=os.listdir('D:\\Project\\cjhbUpdate\\newest\\downloadserver')
mdir.sort()
for edir in mdir:
    root='D:\\Project\\cjhbUpdate\\newest\\downloadserver\\'+edir
    files=edir+".md"
    
    if(len(root)!=0):
        filedir=root+'\\'+files
        file = open(filedir, 'r',encoding='utf-8',errors='ignore')
        data = file.read()
        reg = r'!\[\]\((.*?)\)'
        ia = re.compile(reg)
        datade=data
        sat = re.findall(ia, datade)
        for x in sat:
            reg = r'sign=.*?/(.*?)$'
            ia = re.compile(reg)
            sat2 = re.findall(ia, x)
            if(len(sat2)==0):
                #已经改过
                bar.next()
                continue
            mystr=sat2[0]
            #判断图片是否已经下载完毕
            datade=datade.replace(x,mystr)
            bar.next()
        with open(filedir, "w", encoding="utf-8", errors="ignore") as f2:
            f2.write(datade)
    else:
        print(root)
bar.finish