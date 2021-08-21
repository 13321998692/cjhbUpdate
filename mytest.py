#coding=utf-8

import matplotlib.pyplot as plt
import re
import matplotlib
import datetime

def get_month_range(start_day,end_day):
  months = (end_day.year - start_day.year)*12 + end_day.month - start_day.month
  month_range = ['%s-%s'%(start_day.year + mon//12,mon%12+1) 
                    for mon in range(start_day.month-1,start_day.month + months)]
  return month_range

file = open('pbdate.html', 'rb')
data = file.read()


allold=get_month_range(datetime.date(2015, 1, 1),datetime.date(2020,12,26))
dataa=[]
label=[]

for month in allold:
    reg = r'<td>'+str(month)+'<'
    ia = re.compile(reg)
    sat = re.findall(ia, data.decode('utf-8', errors='ignore'))
    lts = len(sat)
    dataa.append(lts)
    label.append(str(month))
    

for last in range(1,8):
    reg = r'<td>'+str(last)+'-'
    ia = re.compile(reg)
    sat = re.findall(ia, data.decode('utf-8', errors='ignore'))
    lts = len(sat)
    dataa.append(lts)
    label.append("2021-"+str(last))
matplotlib.rcParams['font.sans-serif'] = ['FangSong']
matplotlib.rcParams['font.family']='sans-serif'
plt.bar(label, dataa)
plt.title('纯几何吧发帖数目随时间增长图')

plt.show()