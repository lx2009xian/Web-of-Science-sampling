# -*- coding: utf-8 -*-
'''
***step2：逐一读取链接，返回按引文数量排序的top1-10，median1-10，bottom1-10，30篇文章的title及url
   为step3下载reference做准备'''

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
from lxml import etree
import pandas as pd
import numpy as np

df=pd.read_csv("D:/2020国自然/1-医学或生理学—样本及对照抽样数据/2-按主题抽样(重新设置主题词)/2021.3.17data updata(bottom10%)/number/number.csv")
bro=webdriver.Chrome(executable_path='C:/Users/86198/Desktop/Crawler/chromedriver.exe')
sample_titles=[]
sample_links=[]
for index,url in enumerate(df['total_url']):
        print(index,": doing...")
        bro.get(url)
        top_num=df.loc[index,"top"]
        median_num = df.loc[index, "median"]
        bottom_num = df.loc[index, "bottom"]

        # sample=top_num    #'''!!更改层'''
        # sample=median_num
        sample=bottom_num

        value=int(np.ceil((sample-1)/10))
        page_text = bro.page_source
        tree = etree.HTML(page_text)
        links = []
        titles = []
        bro.find_elements_by_xpath('//li[@aria-label="检索结果排序方式 出版日期: 降序"]')[0].click()
        bro.find_elements_by_xpath('//li[@aria-label="检索结果排序方式 被引频次: 降序"]')[0].click()
        if np.ceil((sample - 1) / 10) +1== np.ceil((sample + 1) / 10):
            page_=bro.find_element_by_xpath('//input[@class="goToPageNumber-input"]')
            page_.clear()
            page_.send_keys(int(value))
            page_.send_keys(Keys.ENTER)
            page_text = bro.page_source
            tree = etree.HTML(page_text)
            page_text = bro.page_source
            tree = etree.HTML(page_text)
            for i in range(int((sample - 1)-(value-1)*10),11):
                for div in tree.xpath('//div[@class="search-results"]'):
                    links.append("https://apps.webofknowledge.com/"+str(div.xpath('./div/div[3]/div/div/div/a/@href')[i-1]))
                    titles.append((bro.find_elements_by_xpath('//a[@class="smallV110 snowplow-full-record"]')[i - 1]).text)
            bro.find_elements_by_xpath('//a[@class="paginationNext snowplow-navigation-nextpage-top"]')[0].click()
            bro.get(bro.current_url)
            page_text = bro.page_source
            tree = etree.HTML(page_text)
            for i in range(1,int(sample+1+1-value*10)):
                for div in tree.xpath('//div[@class="search-results"]'):
                    links.append("https://apps.webofknowledge.com/"+str(div.xpath('./div/div[3]/div/div/div/a/@href')[i-1]))
                    titles.append((bro.find_elements_by_xpath('//a[@class="smallV110 snowplow-full-record"]')[i - 1]).text)
        else:
            page_ = bro.find_element_by_xpath('//input[@class="goToPageNumber-input"]')
            page_.clear()
            page_.send_keys(int(value))
            page_.send_keys(Keys.ENTER)
            bro.get(bro.current_url)
            page_text = bro.page_source
            tree = etree.HTML(page_text)
            for i in range(int((sample - 1)-(value-1)*10), int((sample +2)-(value-1)*10)):
                for div in tree.xpath('//div[@class="search-results"]'):
                    links.append("https://apps.webofknowledge.com/" + str(div.xpath('./div/div[3]/div/div/div/a/@href')[i - 1]))
                    titles.append((bro.find_elements_by_xpath('//a[@class="smallV110 snowplow-full-record"]')[i - 1]).text)
        sample_titles.append(titles)
        sample_links.append(links)
pd.DataFrame(sample_titles).to_csv("D:/2020国自然/1-医学或生理学—样本及对照抽样数据/2-按主题抽样(重新设置主题词)/2021.3.17data updata(bottom10%)/number/title.csv")
pd.DataFrame(sample_links).to_csv("D:/2020国自然/1-医学或生理学—样本及对照抽样数据/2-按主题抽样(重新设置主题词)/2021.3.17data updata(bottom10%)/number/link.csv")
# print(sample_links, sample_titles)
print("结果-2_links.csv/-2titles已生成！")
bro.quit()

# sleep(3)

