from selenium import webdriver
import json
import re
from selenium.webdriver.common.action_chains import ActionChains
from progress.bar import Bar
import os
from time import sleep
import winsound
#初始参数设定

chrome_options = webdriver.ChromeOptions()

#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
#chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])#实现了规避监测
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])#禁止打印日志
driver = webdriver.Chrome(options=chrome_options)  # 使用headless无界面浏览器模式
#driver = webdriver.Chrome()
curpagenum = 1  # 当前处理页面一共多少页


def perror(level):
    winsound.Beep(600,100*level)

def getdate(txt):
    # 将每层的回复信息转化成时间
    reg = r'([0-9]*?楼)(.*?)\n'
    ia = re.compile(reg)
    sa = re.findall(ia, txt)
    if(len(sa)==0):
        exit
    return sa[0][0]+" "+sa[0][1]


def handlehuifu(txt):
    if(txt.find("收起回复") == -1):
        return -1
    relist = txt.split('\n')
    res = ""
    for i in range(len(relist)):
        if i % 2 == 1 and i > 2 and i < len(relist)-3:
            res += relist[i]+"\n"
    return res


def initdriver():
    global driver
    driver.get('https://tieba.baidu.com/')
    sleep(5)
    driver.delete_all_cookies()
    with open('cookies.txt', 'r') as cookief:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookieslist = json.load(cookief)

    for cookie in cookieslist:
        driver.add_cookie(cookie)

def handleneirong(txt):
    result = re.sub(r'<img class="BDE_Smiley".*?>', "", txt)
    result = re.sub(r'<a href=.*?>', "<a>", result)
    result = re.sub(r'<span.*?span>', "", result)
    result = re.sub(r'<em.*?em>', "", result)
    result = re.sub(r'<div.*?>', "", result)
    result = result.replace("<a>", "<")
    result = result.replace("</div>", "")
    result = result.replace("</a>", ">")
    result = result.replace("<br>", "\n")
    reg = r'(<img class="BDE_Image".*?src=").*?(".*?>)'
    ia = re.compile(reg)
    sa = re.findall(ia, result)
    for i in sa:
        result = result.replace(i[0], "![](")
        result = result.replace(i[1], ")")
    return result.strip()


def downloadfirstpage(pageid):
    # 下载pageid页面的内容并生成文字
    global curpagenum
    driver.get('https://tieba.baidu.com/p/'+pageid)
    title = driver.find_element_by_xpath(
        '//*[@id="j_core_title_wrap"]/div[2]/h1').get_attribute("innerText")
    zongyeshu = driver.find_element_by_xpath(
        '//*[@id="thread_theme_5"]/div[1]/ul/li[2]/span[2]').get_attribute("innerText")
    curpagenum = zongyeshu

    finaltext = "# "+title+"\n \n"  # 最终打印
    mco = driver.find_elements_by_class_name("d_post_content")
    
    pti=driver.find_element_by_xpath('//*[@id="head"]/div[1]')
    ActionChains(driver).move_to_element(pti).perform()
    guanggaipos=0
    flag=0
    postlist = []  # 帖子list
    for i in mco:
        try:
            ActionChains(driver).move_to_element(i).perform()
        except Exception as e:
            print(e,pageid)
            perror(3)
        curhtml = i.get_attribute("innerHTML")
        #去除广告
        if(curhtml.find("广告</span>")!=-1):
            guanggaipos=flag
        postlist.append(handleneirong(curhtml))
        flag+=1
    
    mdk = driver.find_element_by_xpath('//*[@id="thread_theme_7"]')
    ActionChains(driver).move_to_element(mdk).perform()

    posterlist = []  # 帖子主list
    mca = driver.find_elements_by_class_name("p_author_name")
    for i in mca:
        curtext = i.get_attribute("innerText")
        posterlist.append(curtext)
    #若有广告，删除
    if(guanggaipos!=0):
        del(postlist[guanggaipos])
        del(posterlist[guanggaipos])

    huifulist = []  # 回复
    louandtime=[]   #记录时间
    mcr = driver.find_elements_by_class_name("core_reply_tail")

    for i in mcr:
        curtext = i.get_attribute("innerText")
        louandtime.append(curtext)
    
    mcrr=driver.find_elements_by_class_name("core_reply")
    for i in mcrr:
        cur=i.get_attribute("innerText")
        huifulist.append(cur)
    
    # 开始生成当前页面的总text
    if(len(postlist) == len(posterlist) and len(posterlist) == len(mcr) and len(mcr)== len(mcrr)):
        for i in range(len(postlist)):
            finaltext += "**"+posterlist[i]+"**:" + \
                postlist[i]+"\n*"+getdate(louandtime[i])+"*\n\n"
            if(handlehuifu(huifulist[i]) != -1):
                finaltext += "**楼回复**：\n"+handlehuifu(huifulist[i])
            finaltext += "\n***\n"
        return finaltext
    else:
        print("error")
        perror(1)
        print(len(postlist), len(posterlist), len(mcr), len(mcrr))
        '''
        for i in mco:
            print(i.get_attribute("innerHTML"))
        print("\n\n")
        for i in mcr:
            print(i.get_attribute("innerText"))
        print("\n\n")
        for i in mcrr:
            print(i.get_attribute("innerText"))
        '''
        return downloadfirstpage(pageid)


def downloadpage(pageid, sid):
    # 下载第sdi页
    print(sid)
    driver.get('https://tieba.baidu.com/p/'+pageid+'?pn='+str(sid))

    finaltext = ""  # 最终打印
    mco = driver.find_elements_by_class_name("d_post_content")
    
    pti=driver.find_element_by_xpath('//*[@id="head"]/div[1]')
    ActionChains(driver).move_to_element(pti).perform()
    guanggaipos=0
    flag=0
    postlist = []  # 帖子list
    for i in mco:
        try:
            ActionChains(driver).move_to_element(i).perform()
        except Exception as e:
            print(e,pageid)
            perror(3)
        curhtml = i.get_attribute("innerHTML")
        postlist.append(handleneirong(curhtml))
        #去除广告
        if(curhtml.find("广告</span>")!=-1):
            guanggaipos=flag
        flag+=1

    mdk = driver.find_element_by_xpath('//*[@id="thread_theme_7"]')
    ActionChains(driver).move_to_element(mdk).perform()

    posterlist = []  # 帖子主list
    mca = driver.find_elements_by_class_name("p_author_name")
    for i in mca:
        curtext = i.get_attribute("innerText")
        posterlist.append(curtext)
    
    if(guanggaipos!=0):
        del(postlist[guanggaipos])
        del(posterlist[guanggaipos])
    huifulist = []  # 回复
    louandtime=[]   #记录时间
    mcr = driver.find_elements_by_class_name("core_reply_tail")

    for i in mcr:
        curtext = i.get_attribute("innerText")
        louandtime.append(curtext)
    
    mcrr=driver.find_elements_by_class_name("core_reply")
    for i in mcrr:
        cur=i.get_attribute("innerText")
        huifulist.append(cur)

    # 开始生成当前页面的总text

    if(len(postlist) == len(posterlist) and len(postlist) == len(mcr) and len(mcr)== len(mcrr)):
        for i in range(len(postlist)):
            finaltext += "**"+posterlist[i]+"**:" + \
                postlist[i]+"\n*"+getdate(louandtime[i])+"*\n\n"
            if(handlehuifu(huifulist[i]) != -1):
                finaltext += "**楼回复**：\n"+handlehuifu(huifulist[i])
            finaltext += "\n***\n"
        return finaltext
    else:
        print("error")
        print(len(postlist), len(posterlist), len(mcr))
        perror(1)
        return downloadpage(pageid, sid)


initdriver()  # 初始化

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
try:
    for x in sat:
        if(os.path.exists('downloadserver/'+str(x)+'/'+str(x)+'.md')):
            bar.next()
            continue
        if (not os.path.exists('downloadserver/'+str(x))):
            os.mkdir('downloadserver/'+str(x))
        #开始下载
        thispage = str(x)
        # 首页下载
        fpage = downloadfirstpage(thispage)
        # 下载剩余
        for i in range(2, int(curpagenum)+1):
            fpage += downloadpage(thispage, i)
        with open("downloadserver/"+thispage+'/'+thispage+'.md', "w", encoding="utf-8", errors="ignore") as f2:
            f2.write(fpage)
        bar.next()
except Exception as e:
    driver.quit()
    perror(30)
    print(e)
    print(x)
    exit
bar.finish
'''

#测试用单体实验
fp=downloadfirstpage("6081045912")
with open("down.md", "w", encoding="utf-8", errors="ignore") as f2:
    f2.write(fp)
'''
driver.quit()  # 结束进程