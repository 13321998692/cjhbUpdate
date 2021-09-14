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
bar = Bar('Processing', max=13000,
          suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')
full=0
for root, dirs, files in os.walk('D:\\Project\\cjhbUpdate\\newest\\downloadserver'):
    #print(root)
    #print(files)
    
    if(len(root)!=0 and len(files)!=0):
        for xs in files:
            if(xs[-2:]=='md'):
                filedir=root+'\\'+xs
                file = open(filedir, 'rb')
                data = file.read()
                reg = r'!\[\]\((.*?)\)'
                ia = re.compile(reg)
                datade=data.decode(encoding='utf-8',errors='ignore')
                sat = re.findall(ia, datade)
                for x in sat:
                    #print(x)
                    #print(root,str(x))
                    reg2 = r'sign=.*?\/(.*?jpg)'
                    ia2 = re.compile(reg2)
                    sat2 = re.findall(ia2, x)
                    if(os.path.exists(root+'\\'+sat2[0])):
                        bar.next()
                        continue
                    doen='http://tiebapic.baidu.com/forum/pic/item/'+sat2[0]
                    #print(root)
                    #二次下载后处理异常
                    print(x)
                    #IDMdownload(x,root,sat2[0])
                    bar.next()
    else:
        print(root)
bar.finish