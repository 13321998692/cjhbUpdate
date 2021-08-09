# coding=utf-8
import requests
from progress.bar import Bar
from bs4 import BeautifulSoup
import os
import re
import shutil

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

swr = '''
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<title>纯几何吧主题贴检索</title>
<link rel="icon" href="favicon.ico" type="image/ico">
<link href="../css/bootstrap.min.css" rel="stylesheet">
<link href="../css/materialdesignicons.min.css" rel="stylesheet">
<link href="../css/style.min.css" rel="stylesheet">
'''

fi = '''
<table class="table table-striped">
<tr>
<th>标题</th>
<th>标签</th>
<th>时间</th>
</tr>
'''

cookies = {
    'PSTM': '1628174644',
    'BAIDUID': '461218646534E0FDC31D373550706CF4:FG=1',
    'BIDUPSID': '8014F6D7BFA37DC87A5BF49985C84287',
    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
    '__yjs_duid': '1_be83af0d77043f30fc776d9513ecdeec1628174652362',
    'BDUSS': 'lEtYnRlVDhoMi02WHplandEbUN-dWFieVdUUXNtam9SbXhFVllBU3Z2MGNoek5oRVFBQUFBJCQAAAAAAAAAAAEAAADRKZukMTMzX0JBXzk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABz6C2Ec-gthZ',
    'BDUSS_BFESS': 'lEtYnRlVDhoMi02WHplandEbUN-dWFieVdUUXNtam9SbXhFVllBU3Z2MGNoek5oRVFBQUFBJCQAAAAAAAAAAAEAAADRKZukMTMzX0JBXzk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABz6C2Ec-gthZ',
    'STOKEN': 'a40d55ef379d56900e4d7c417479b9b2bf9d09227ef2f85dbe49e1ebb9482609',
    'bdshare_firstime': '1628227231590',
    'BAIDUID_BFESS': '461218646534E0FDC31D373550706CF4:FG=1',
    'BAIDU_WISE_UID': 'wapp_1628498789907_927',
    'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948': '1628498993,1628499684,1628501803,1628506111',
    'st_key_id': '17',
    'USER_JUMP': '-1',
    'ab_sr': '1.0.1_MzRhY2ZiZmM3MzQ0ZDUyZjI5ODY0NTU1YzlkNjQzOGUzOWM4NTE5ZGRkYzNlMDU5ZTk4ZDk2ODJhMWI1MjEzMDMwMTUxMTViMjVmOWQ4ZTcxNDI5M2JhNDE0NzQ5OTJmNDNjOTUxOTYzZDRiNmNiNTBjY2NmOTY5ZjM3ODQ2YjUzNGJiYmMwOTdkMzgwMDI4ODYxM2U5NzEwOTBmNzExYmEyZDRkZDI0ZDBkMDMxOWE5NzYyNjM1NmMyMzU1YWZm',
    'st_data': 'a9712517b40ee61c2708af9db58f92235ffaebff39ddbf6f0a5a0d019614fe4c6d954352aec1352589884507c091cca06ef2ab7831f4457b490a50910ca4f4aac46c4f70e39e2e0a3dbd3a0659ad51990da755b3afa27653bb67a1a108a8268a8c344f5f4067f83df88cae0f90136f53bb2664441c0229bdf65b8e1bc30212e00402f95c621ccf305dfd89808497a7c4',
    'st_sign': 'e11a16c4',
    'tb_as_data': 'f88f3dc9e487d651ec8f122c218a99998919e7454cf19eca0c69c80a508caa01c52d66bea45be75e4b06f591a924389a7cd7223c129696d093ad5a711a0cc817c30e0f01db06b94538a5e23cf69b39812e97726c0796033cb9f6393ca683d36cfae4c2042013bd9dd84a64e74d5ef231',
    'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948': '1628506122',
}



k = 1
file = open('pb.html', 'rb')
data = file.read()
reg = r'/p/(.*?)"'
ia = re.compile(reg)
sat = re.findall(ia, data.decode('utf-8', errors='ignore'))
lts = len(sat)
if (not os.path.exists('downloadserver')):
    os.mkdir('downloadserver')
bar = Bar('Processing', max=lts,
          suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')

for x in sat:
    if(os.path.exists('downloadserver/'+str(x)+'/'+str(x)+'.html')):
        bar.next()
        k = k+1
        continue
    ktmp = 1
    while (ktmp == 1):
        try:
            file = requests.get("http://tieba.baidu.com/p/" +
                                str(x), headers=headers, cookies=cookies)
            data = file.content
            ktmp = 0
        except Exception as e:
            ktmp = 1
    if(not os.path.exists('downloadserver/'+str(x))):
        os.mkdir('downloadserver/'+str(x))

    soup = BeautifulSoup(data, 'html.parser')
    temp = soup.find(attrs={"class": "core_title_txt"})
    nstr = bytes('百度安全验证', encoding='UTF-8')
    fres = data.find(nstr, 0, len(data))
    if (fres != -1):
        print("请刷新cookie!")
        exit()
    if temp == None:
        bar.next
        continue
    final = temp.string
    for ash in soup.findAll(attrs={"class": "d_post_content"}):
        if ash.contents!=None:
            result = re.sub(r'\<.*?\>', "",str(ash.contents))
            result2 = re.sub(r' ', "",result)
            result3 =re.sub(r',', "",result2)
            final+=result3
    with open('downloadserver/'+str(x)+'/'+str(x)+'.html', "w", encoding="utf-8", errors="ignore") as f2:
        f2.write(final)
    bar.next()
    k = k+1
k = 1
bar.finish
print("页面下载完成1，开始处理writer")

if(os.path.exists('./writer')):
    shutil.rmtree('./writer')
if(os.path.exists('./userinfo.txt')):
    os.remove('./userinfo.txt')
os.mkdir('writer')

reg = r'/p/(.*?)">(.*?)</a>[\s\S]*?<td>(.*?)</td>[\s\S]*?writer/(.*?)\.html"[\s\S]*?<td>(.*?)</td>'
ia = re.compile(reg)
nhtml = requests.get(
    "http://www.yydbxx.cn/t/pb.html").content.decode(encoding='utf-8', errors='ignore')
taglist = re.findall(ia, nhtml)

bar = Bar('Processing', max=len(taglist),
          suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')

for x in taglist:
    thisname=x[3].encode(encoding="utf-8",errors="ignore").decode(encoding="utf-8",errors="ignore")
    if (not os.path.isfile('./writer/'+thisname+'.html')):
        fhandle = open('./writer/'+thisname+'.html', 'a',encoding="utf-8")
        fhandle.write(swr+'<div align="center"> <h1>' +
                      thisname+'</h1></div>\n'+fi)
        fhandle.close()
        fhandle = open('userinfo.txt', 'a',encoding="utf-8")
        fhandle.write('<'+thisname+'>\n')
        fhandle.close()
    fhandle = open('./writer/'+thisname+'.html', 'a',encoding="utf-8")
    thistag=x[2].replace("./tags","../tags")
    fhandle.write('<tr>\n<td><a href="http://tieba.baidu.com/p/'+x[0]+'">'+
                x[1]+'</a></td>\n<td>'+thistag+'</td><td><a href="writer/'+thisname+'.html">'+thisname+'</a></td>\n<td>'+str(x[4])+'</td>\n</tr>\n')
    fhandle.close()
    bar.next()
print('\n Success!\n')

bar.finish
