# coding=utf-8
from progress.bar import Bar
import requests
import re
import os
import ast

swr = '''
<!DOCTYPE html>
<html lang="zh">
<head>
<script src="http://www.yydbxx.cn/res/jquery.min.js"></script>
<script type="text/javascript">
function se(){
	var s=document.getElementById("eti").value;
	if(s==''){
	alert("不能为空");
	returrn;	
	}
	
	var sa=document.getElementById("ss").value;
	if(sa=="0"){
		window.location.href="./ri.php?ssid="+s;
	}
	if(sa=="1"){
		window.location.href="./riauthor.php?ssid="+s;
	}
	if(sa=="2"){
		window.location.href="./com.php?ssid="+s;
	}
if(sa=="3"){
		window.location.href="./ritag.php?ssid="+s;
	}
}
	
	$(document).ready(function(){

	$('#eti').bind('keydown',function(event){  
        	        if(event.keyCode == "13")      
        	        {  
		se();
		}
});
});
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<title>纯几何吧题目检索</title>
<link rel="icon" href="favicon.ico" type="image/ico">
<link href="css/bootstrap.min.css" rel="stylesheet">
<link href="css/materialdesignicons.min.css" rel="stylesheet">
<link href="css/style.min.css" rel="stylesheet">
<div align="center"> <h1>纯几何吧题目检索</h1></div>
<div align="center" style="width:100%"><h4>更新于2020.7.25(v1.7)</h4>
<div style="width:60%;float:left;">
<input class="form-control" type="text" id="eti" name="example-text-input" placeholder="请输入搜索内容...">
</div>
<div style="width:30%;float:left;">
<select class="form-control" id="ss" name="example-select" size="1">
                        <option value="0">按题目搜索</option>
                        <option value="1">按作者搜索</option>
			<option value="2">按内容搜索</option>
			<option value="3">按标签搜索</option>
</select>
</div>
</div>
</br></br>
<div align="center">
<button class="btn btn-default btn-w-md" type="button" onclick="se()">搜索</button>
</div>
</br>
<p style="text-align:center">常用标签：<a href="tags/题面简单.html">题面简单</a> <a href="tags/我们爱几何.html">我们爱几何</a> <a href="tags/射影.html">射影</a> <a href="tags/单圆问题.html">单圆问题</a> (感谢djc提供的标签数据！)</p>
<table class="table table-striped">
<tr>
<th>题目</th>
<th>标签</th>
<th>作者</th>
<th>时间</th>
</tr>
'''

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
    'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948': '1628232398,1628232992,1628233921,1628340185',
    'st_key_id': '17',
    'wise_device': '0',
    'st_data': 'a9712517b40ee61c2708af9db58f92239b830ae9420f01dfabe564675b8a1aceafd42accebcbead9f2a3be3e4fcf316910feddf116b73dc904f35b1d6024fd8c692a1c9c5a604c988dc1d9e44dafefbc3f2b1b7debdb4dadfe777a417b47fb8371653d3f04e05f201c523f4bd1badedd67561814ca92a7bd0ce9d1cfac82dd9d',
    'st_sign': '16214376',
    'ab_sr': '1.0.1_NWE1MzAxMzRkMWEyNmM3ZDQ0ODRlNjcyZTA4MGNkZDFmZTE1OGM0NzVkZTJhYTIwY2JhMDQ4ZGEzOWRhNGFhN2Y5MmJiOGEwNGRmN2Y4MzYwZGI3NTY1YzdkMWMwNDdkMGQ5MGVlNWQ1ZGNkMWE3OWI3NjExYThmNTcwZWUzNjBkMWM4ZWNhMmMxNmVkOTg5NzdkMDExZWRhMTU2ZDg0NA==',
    'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948': '1628340212',
}



ktmp = 1
while (ktmp == 1):
    try:
        file = requests.get("http://tieba.baidu.com/f?kw=许氏数学")
        data = file.content.decode(encoding="utf-8", errors="ignore")
        #print(data)
        ktmp = 0
    except Exception as e:
        mydata = input()
        cookies = ast.literal_eval(mydata)
        ktmp = 1
reg = r'pn=(.*?)" class="last pagination-item " >尾页'
ia = re.compile(reg)
sa = re.findall(ia, data)
maxpage = 0
for x in sa:
    maxpage = int(x)
print('总页数为：'+str(maxpage))
k = 0
list = []

bar=Bar('Processing',max=maxpage/50+1,suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')
while k<=maxpage:
	ktmp=1
	while (ktmp==1):
		try:
			file=requests.get("http://tieba.baidu.com/f?kw=许氏数学&ie=utf-8&pn="+str(k))
			data=file.content.decode(encoding="utf-8", errors="ignore")
			ktmp=0
		except Exception as e:
			ktmp=1
	reg=r'href="/p/(.+?)" title="(.+?)".*?j_th_tit[\s\S]*?主题作者: (.+?)"[\s\S]*?创建时间">(.+?)<'
	ia=re.compile(reg)
	sa=re.findall(ia,data)
	list=list + sa
	bar.next()
	k=k+50
list=sorted(list, key=lambda i:int(i[0]))
fhandle=open('./pb.html','w',encoding='utf-8',errors='ignore')
fhandle.write(swr)
for x in list:
	fhandle.write('<tr>\n<td><a href="http://tieba.baidu.com/p/'+str(x[0])+'">'+str(x[1])+'</a></td>\n<td></td><td>><a href="writer/'+str(x[2])+'.html">'+str(x[2])+'</a></td>\n<td>'+str(x[3])+'</td>\n</tr>\n')
fhandle.write('</table>')
fhandle.close()
bar.finish
'''
<tr>
<td><a href="http://tieba.baidu.com/p/6835689892">4478重发</a></td>
<td></td><td><a href="writer/◆qzc◆.html">◆qzc◆</a></td>
<td>7-24</td>
</tr>
'''