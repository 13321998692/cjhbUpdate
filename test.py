#coding=utf-8
import re
import requests

reg = r'/p/(.*?)">(.*?)</a>[\s\S]*?<td>(.*?)</td>[\s\S]*?writer/(.*?)\.html"[\s\S]*?<td>(.*?)</td>'
ia = re.compile(reg)
nhtml = requests.get(
    "http://www.yydbxx.cn/t/pb.html").content.decode(encoding='utf-8', errors='ignore')
taglist = re.findall(ia, nhtml)
print(len(taglist))