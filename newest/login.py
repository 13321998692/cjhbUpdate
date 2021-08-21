#coding=utf-8
import time
import json
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://tieba.baidu.com/')

time.sleep(30)

with open('cookies.txt','w') as cookief:
    #将cookies保存为json格式
    cookief.write(json.dumps(driver.get_cookies()))
driver.close()