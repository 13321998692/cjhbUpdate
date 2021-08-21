#coding=utf-8

import re

def getdate(txt):
    if(txt.find("我也说一句\n\n还有")!=-1):
        #特殊处理
        relist=txt.split('\n')
        res=""
        for i in range(len(relist)):
            if i%2==1 and i>2 and i<len(relist)-2:
                res+=relist[i]+"\n"
        return res
    relist=txt.split('\n')
    res=""
    for i in range(len(relist)):
        if i%2==1 and i>2 and i<len(relist)-1:
            res+=relist[i]+"\n"
    return res
def handleneirong(txt):
    result=re.sub(r'<img class="BDE_Smiley".*?>',"",txt)
    result=re.sub(r'<a href=.*?>',"<a>",result)
    result=re.sub(r'<span.*?span>',"",result)
    result=re.sub(r'<em.*?em>',"",result)
    result=re.sub(r'<div.*?>',"",result)
    result=result.replace("<a>","<")
    result=result.replace("</div>","")
    result=result.replace("</a>",">")
    result=result.replace("<br>","\n")
    reg = r'(<img class="BDE_Image".*?src=").*?(".*?>)'
    ia = re.compile(reg)
    sa = re.findall(ia, result)
    for i in sa:
        result=result.replace(i[0],"![](")
        result=result.replace(i[1],")")
    return result.strip()
curhtml='''
<img class="BDE_Image" pic_type="0" width="560" height="446" src="https://imgsa.baidu.com/forum/w%3D580/sign=e061007ff1d3572c66e29cd4ba126352/ee3734cad1c8a78623a71d986409c93d71cf5044.jpg" pic_ext="jpeg">
<img class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=4e87e5865a2c11dfded1bf2b53266255/5ee270c8a786c9175360705cc43d70cf3bc75718.jpg" size="3075213" changedsize="true" width="560" height="420">
<img class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=5b575aaf5c3d26972ed3085565fab24f/33f47000baa1cd1189301545b412c8fcc2ce2dfe.jpg" size="45752" width="477" height="246">'''

print(handleneirong(curhtml))