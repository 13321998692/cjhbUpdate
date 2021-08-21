#coding=utf-8
from progress.bar import Bar
import os
import re
maxi=0
def IDMdownload(DownUrl, DownPath, FileName):
    IDMPath = "C:\\Program Files (x86)\\Internet Download Manager\\"
    os.chdir(IDMPath)
    IDM = "IDMan.exe"
    command = ' '.join([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/a', '/d'])
    os.system(command)
bar = Bar('Processing', max=10000,
          suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')
full=0
for root, dirs, files in os.walk('D:\\Project\\cjhbUpdate\\newest\\downloadserver'):
    #print(root)
    #print(files)
    if(len(root)!=0 and len(files)!=0):
        filedir=root+'\\'+files[0]
        file = open(filedir, 'r',encoding='utf-8',errors='ignore')
        data = file.read()
        reg = r'!\[\]\((.*?)\)'
        ia = re.compile(reg)
        datade=data
        sat = re.findall(ia, datade)
        for x in sat:
            print(x)
    else:
        print(root)
bar.finish