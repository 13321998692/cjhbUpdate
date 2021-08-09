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
<style>
    .container {
      height: 100%;
      width: 100%;
      align-items: center;
    }

    .bgDiv {
      box-sizing: border-box;
      width: 60%;
      position: relative;
      float: left;
    }

    .search-input-text {
      border: 1px solid #b6b6b6;
      width: 100%;
      background: #fff;
      height: 33px;
      line-height: 33px;
      font-size: 18px;
      padding: 3px 0 0 7px;
    }

    .suggest {
        width: 100%;
      position: absolute;
      top: 38px;
      border: 1px solid #999;
      background: #fff;
      display: none;
    }

    .suggest ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .suggest ul li {
      padding: 3px;
      font-size: 17px;
      line-height: 25px;
      cursor: pointer;
    }

    .suggest ul li:hover {
      background-color: #b6b6b6;
    }
  </style>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<title>纯几何吧题目检索</title>
<link rel="icon" href="favicon.ico" type="image/ico">
<link href="css/bootstrap.min.css" rel="stylesheet">
<link href="css/materialdesignicons.min.css" rel="stylesheet">
<link href="css/style.min.css" rel="stylesheet">
<div align="center"> <h1>纯几何吧题目检索</h1></div>
<div align="center" style="width:100%"><h4>更新于2021.8.8(v1.8)</h4>
<div class="container">
    <div class="bgDiv">
        <input class="form-control search-input-text" type="text" id="eti" name="example-text-input" placeholder="请输入搜索内容...">
        <div class="suggest">
            <ul id="search-result">
            </ul>
        </div>
    </div>
    <div style="width:30%;float:right;">
        <select class="form-control" id="ss" name="example-select" size="1">
                                <option value="0">按题目搜索</option>
                                <option value="1">按作者搜索</option>
                    <option value="2">按内容搜索</option>
                    <option value="3">按标签搜索</option>
        </select>
        </div>
</div>


</div>
<script>
    var suggestContainer = document.getElementsByClassName("suggest")[0];
    var searchInput = document.getElementsByClassName("search-input-text")[0];
    var bgDiv = document.getElementsByClassName("bgDiv")[0];
    var searchResult = document.getElementById("search-result");
    var sa=document.getElementById("ss").value;
    var currentlink="";
    // 清除建议框内容
    function clearC(){
        suggestContainer.style.display = "none";
        clearContent;
    }

    function clearContent() {
      var size = searchResult.childNodes.length;
      for (var i = size - 1; i >= 0; i--) {
        searchResult.removeChild(searchResult.childNodes[i]);
      }
    };

    var timer = null;
    // 注册输入框键盘抬起事件
    searchInput.onkeyup = function (e) {
        sa=document.getElementById("ss").value;
        if(sa!=0 && sa!=1){
            return;
        }
        if(sa==1){
            //作者
            suggestContainer.style.display = "block";
            // 如果输入框内容为空 清除内容且无需跨域请求
            if (this.value.length === 0) {
                suggestContainer.style.display = "none";
                clearContent();
                return;
            }
            if (this.timer) {
                clearTimeout(this.timer);
            }
            if (e.keyCode !== 40 && e.keyCode !== 38 && e.keyCode !== 37 && e.keyCode !== 39) {
                // 函数节流优化
                this.timer = setTimeout(() => {
                // 创建script标签JSONP跨域
                var script = document.createElement("script");
                script.src = "http://www.yydbxx.cn/t/sriauthor.php?ssid=" + encodeURI(this.value.trim());
                document.body.appendChild(script);
                }, 130)
            }
            return;
        }
      suggestContainer.style.display = "block";
      // 如果输入框内容为空 清除内容且无需跨域请求
      if (this.value.length === 0) {
        suggestContainer.style.display = "none";
        clearContent();
        return;
      }
      if (this.timer) {
        clearTimeout(this.timer);
      }
      if (e.keyCode !== 40 && e.keyCode !== 38 && e.keyCode !== 37 && e.keyCode !== 39) {
        // 函数节流优化
        this.timer = setTimeout(() => {
          // 创建script标签JSONP跨域
          var script = document.createElement("script");
          script.src = "http://www.yydbxx.cn/t/sri.php?ssid=" + encodeURI(this.value.trim());
          document.body.appendChild(script);
        }, 130)
      }

    };

    // 回调函数处理返回值
    function handleSuggestion(res) {
    //console.log(res);
      // 清空之前的数据！！
      clearContent();
      var result = res.s;
      var myhtml=res.h;
      // 截取前五个搜索建议项
      if (result.length > 5) {
        result = result.slice(0, 6)
      }
      for (let i = 0; i < result.length; i++) {
        // 动态创建li标签
        var liObj = document.createElement("li");
        liObj.innerHTML = result[i];
        liObj.id=myhtml[i];
        searchResult.appendChild(liObj);
      }
    }


    function jumpPage() {
        sa=document.getElementById("ss").value;
        if(sa==1){
            //author
            window.open(`http://www.yydbxx.cn/t/writer/${encodeURI(currentlink+".html")}`);
            return;
        }
      window.open(`http://www.tieba.com/p/${encodeURI(currentlink)}`);
    }

    // 事件委托 点击li标签
    bgDiv.addEventListener("click", function (e) {
        clearContent();
      if (e.target.nodeName.toLowerCase() === 'li') {
        var keywords = e.target.innerText;
        searchInput.value = keywords;
        currentlink=e.target.id;
        jumpPage();
      }
      
    }, false);

    var i = 0;
    var flag = 1;

    // 事件委托 监听键盘事件
    bgDiv.addEventListener("keydown", function (e) {
      var size = searchResult.childNodes.length;
      // 键盘向下事件
      if (e.keyCode === 40) {
        if (flag === 0) {
          i = i + 2;
        }
        flag = 1;
        e.preventDefault();
        if (i >= size) {
          i = 0;
        }
        if (i < size) {
          searchInput.value = searchResult.childNodes[i++].innerText;
          currentlink=searchResult.childNodes[i++].id;
          i--;
        }
      };
      // 键盘向上事件
      if (e.keyCode === 38) {
        if (flag === 1) {
          i = i - 2;
        }
        flag = 0;
        e.preventDefault();
        if (i < 0) {
          i = size - 1;
        }
        if (i > -1) {
          searchInput.value = searchResult.childNodes[i--].innerText;
          currentlink=searchResult.childNodes[i--].id;
          i++;
        }
      };
    }, false);

    // 点击页面任何其他地方 搜索结果框消失

    document.onclick = () => clearC()

  </script>
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
    'BAIDU_WISE_UID': 'wapp_1628407474377_286',
    'showCardBeforeSign': '1',
    'Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948': '1628407474,1628436338,1628436863,1628462678',
    'USER_JUMP': '-1',
    'st_key_id': '17',
    'H_PS_PSSID': '34398_34333_34369_31660_34405_34004_34092_26350',
    'delPer': '0',
    'PSINO': '6',
    'BA_HECTOR': 'ah018k0h85a40020or1gh0oog0r',
    'ab_sr': '1.0.1_MjFhMmYyOGQ2YWU0MTg0NTI0NjA3YzI4OWY2ZjgzZGIyMWEwYzUxYjk1MGRjYTg1YmI2ZmJhZDU0ZWRmNjYzN2U0ZDQ0ZjgyYTY2OWZhNWI4MWEzNWFlMTZiMmJhZDBjOTM4NzA2OGNjMjQyZTA3YWIxZWEwYjY5MGYxYzU0OGNlYTI3MzBlY2NiMjJhYjQyZjhjOWVkZjVhMDM3OWVlNjY0NTI4NzM2OTQyNGE2YjA1ZjQ1ZDc1ZDgwM2FjOTM1',
    'st_data': 'a9712517b40ee61c2708af9db58f92235ffaebff39ddbf6f0a5a0d019614fe4c6d954352aec1352589884507c091cca06ef2ab7831f4457b490a50910ca4f4aac46c4f70e39e2e0a3dbd3a0659ad51990da755b3afa27653bb67a1a108a8268a6026f264daf2ac719541796092004ac8bb043943e92a280016e9ae4f7b01f804716ca5a3b279ebb9913777805afc0dc6',
    'st_sign': '929041ac',
    'tb_as_data': 'f88f3dc9e487d651ec8f122c218a99998919e7454cf19eca0c69c80a508caa01c52d66bea45be75e4b06f591a924389a7cd7223c129696d093ad5a711a0cc817833f6e799ec9d049fc79a642652fc533dcc593ee4069d5845c45964b8d3016a1e9321e0385a588976a77c7881e10b541',
    'Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948': '1628463966',
}

ktmp = 1
while (ktmp == 1):
    try:
        file = requests.get("http://tieba.baidu.com/f?kw=纯几何",
                            headers=headers, cookies=cookies)
        data = file.content.decode(encoding="utf-8", errors="ignore")
        ktmp = 0
    except Exception as e:
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

bar = Bar('Processing', max=maxpage/50+1,
          suffix='%(index)d/%(max)d - %(percent).2f%% - [%(elapsed)ds<%(eta)ds]')
while k <= maxpage:
    ktmp = 1
    while (ktmp == 1):
        try:
            file = requests.get("http://tieba.baidu.com/f?kw=纯几何&ie=utf-8&pn=" +
                                str(k), headers=headers, cookies=cookies)
            data = file.content.decode(encoding="utf-8", errors="ignore")
            ktmp = 0
        except Exception as e:
            ktmp = 1
    reg = r'href="/p/(.+?)" title="(.+?)".*?j_th_tit[\s\S]*?主题作者: (.+?)"[\s\S]*?创建时间">(.+?)<'
    ia = re.compile(reg)
    sa = re.findall(ia, data)
    list = list + sa
    bar.next()
    k = k+50
list = sorted(list, key=lambda i: int(i[0]))

#判断新帖子


fhandle = open('./pb.html', 'w', encoding='utf-8', errors='ignore')
fhandle.write(swr)
nhtml = requests.get(
    "http://www.yydbxx.cn/t/pb.html").content.decode(encoding='utf-8', errors='ignore')

reg = r'/p/(.*?)".*?</td>[\s\S][\s\S]<td>(\|.*?)</td>'
ia = re.compile(reg)
taglist = re.findall(ia, nhtml)

for x in list:
    fres = nhtml.find(str(x[0]), 0, len(nhtml))
    if (fres != -1):
        # 判断是否有tag
        flag = 0
        thistag = ''
        for tag in taglist:
            if tag[0] == str(x[0]):
                flag = 1
                thistag = tag[1]
                break
        if flag == 1:
            # tag
            fhandle.write('<tr>\n<td><a href="http://tieba.baidu.com/p/'+str(x[0])+'">'+str(
                x[1])+'</a></td>\n<td>'+thistag+'</td><td><a href="writer/'+str(x[2])+'.html">'+str(x[2])+'</a></td>\n<td>'+str(x[3])+'</td>\n</tr>\n')
            continue
    fhandle.write('<tr>\n<td><a href="http://tieba.baidu.com/p/'+str(x[0])+'">'+str(
        x[1])+'</a></td>\n<td></td><td><a href="writer/'+str(x[2])+'.html">'+str(x[2])+'</a></td>\n<td>'+str(x[3])+'</td>\n</tr>\n')
fhandle.write('</table>')
fhandle.close()
bar.finish
