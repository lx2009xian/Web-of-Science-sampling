'''
***step1：wos内完成高级检索，返回检索结果链接
   先构造好检索式，保证读入的均是合法构造的检索式，否则中途程序退出需要重新跑'''

from selenium import webdriver
from time import sleep
import pandas as pd
from lxml import etree
import numpy as np
url='http://apps.webofknowledge.com/WOS_AdvancedSearch_input.do?SID=7ElP2sCQwzO9mq6MOcl&product=WOS&search_mode=AdvancedSearch'
bro=webdriver.Chrome(executable_path='C:/Users/86198/Desktop/Crawler/chromedriver.exe')
bro.get(url)

file="D:/2020国自然/1-医学或生理学—样本及对照抽样数据/2-按主题抽样(重新设置主题词)/2021.3.17data updata(bottom10%)/data/8.csv"
# df=pd.read_excel(file,sheet_name="Control Group(top10%)")
df=pd.read_csv(file)

for i,item in enumerate(list(df['request'])):
    search_input=bro.find_element_by_id('value(input1)')
    search_input.clear()
    search_input.send_keys(item)
    btn=bro.find_element_by_id('search-button')
    btn.click()
    print(i,": done！")

page_text=bro.page_source
tree=etree.HTML(page_text)
list=tree.xpath('//div[@class="historyResults"]')
for t in list:
    list_index = int((t.xpath('./@id')[0].replace("set_","")).replace("_div",""))
    df.loc[(list_index-1),"total_url"]="https://apps.webofknowledge.com/"+str(t.xpath('./a/@href')[0])
    if "," in t.xpath('./a/text()')[0]:
        df.loc[(list_index-1),"total"]=int(t.xpath('./a/text()')[0].replace(",",""))
    else:
        df.loc[(list_index-1),"total"]=int(t.xpath('./a/text()')[0])

#求top,median,bottom
df.top=np.ceil(df["total"]/20)
df["median"]=np.ceil(df["total"]*0.5)
df.bottom=np.ceil(df["total"]*0.95)

df.to_csv("D:/2020国自然/1-医学或生理学—样本及对照抽样数据/2-按主题抽样(重新设置主题词)/2021.3.17data updata(bottom10%)/number/number.csv")
sleep(2)
print("检索结果-1.csv已生成！")
bro.quit()
