# -*- coding: utf-8 -*-
'''  step3：逐一下载top1-10，median1-10，bottom1-10，各30篇文章的reference
'''

from selenium import webdriver
from time import sleep
from lxml import etree
import pandas as pd
import re

df=pd.read_csv("D:/2020国自然/1-医学或生理学—样本及对照抽样数据/2-按主题抽样(重新设置主题词)/2021.3.17data updata(bottom10%)/number/link.csv")   #读取top、median、bottom各十篇对照的url
for i in range(0,df.shape[0]):
# for i in range(5,21):      #行，从第0行开始，若因为网络原因中途退出，修改范围接着跑
    for j in range(1,df.shape[1]):  #列，从第1列开始
        url=df.iloc[i,j]
        bro = webdriver.Chrome(executable_path='C:/Users/86198/Desktop/Crawler/chromedriver.exe')
       # url="https://apps.webofknowledge.com/full_record.do?product=WOS&search_mode=GeneralSearch&qid=1&SID=E45TARJuNVgKOfAPSDm&page=1&doc=1"
        bro.get(url)
        #sleep(10)
        tree=etree.HTML(bro.page_source)
        if int(re.findall("\d+",bro.find_element_by_xpath('//h2').get_attribute('textContent'))[0]) == 0:
            print("index:",i,"sample_index:",j,"no reference!")
            bro.quit()
        else:
            ref=tree.xpath('//a[@class="view-all-link snowplow-view-all-in-cited-references-page-top"]')
            ref_url = "https://apps.webofknowledge.com//"+str(ref[0].xpath('./@href')[0])
            bro.get(ref_url)
            flag=0
            while int(bro.find_element_by_xpath("//input[@class='goToPageNumber-input']").get_attribute("value")) < int(bro.find_element_by_xpath('//span[@id= "pageCount.top"]').get_attribute('textContent')):
                bro.find_elements_by_xpath('//button[@class="onload-secondary-button addToMarkedList"]')[0].click()
                bro.find_elements_by_xpath('//input[@id="numberOfRecordsAllOnPage"]')[0].click()
                bro.find_elements_by_xpath('//button[@id="markedListButton"]')[0].click()
                bro.find_elements_by_xpath('//a[@class="paginationNext snowplow-navigation-nextpage-top"]')[0].click()
            if int(bro.find_element_by_xpath("//input[@class='goToPageNumber-input']").get_attribute("value"))== int(bro.find_elements_by_xpath('//span[@id= "pageCount.top"]')[0].get_attribute('textContent')):
                bro.find_elements_by_xpath('//button[@class="onload-secondary-button addToMarkedList"]')[0].click()
                bro.find_elements_by_xpath('//input[@id="numberOfRecordsAllOnPage"]')[0].click()
                bro.find_elements_by_xpath('//button[@id="markedListButton"]')[0].click()
            bro.find_elements_by_xpath('//a[@title="标记结果列表"]')[0].click()
            if int(re.findall("\d+", bro.find_elements_by_xpath('//div[@class="NEWpageTitle"]')[0].text)[0])==0:
                print("index:",i,"sample_index:",j,"no reference!")
                bro.quit()
            else:
                # bro.find_elements_by_xpath('//button[@class="onload-secondary-button exportIconButton nav-link"]')[0].click()
                # bro.find_elements_by_xpath('//a[@title="将所选记录导出至制表符分隔文件、其他参考文件软件等"]')[0].click()
                # bro.find_elements_by_xpath('//span[@id="select2-saveOptions-container"]')[0].click()
                # bro.find_elements_by_xpath('//li[contains(text(), "纯文本")]')[0].click()
                bro.find_elements_by_xpath('//button[@title="保存到 Excel 文件"]')[0].click()
                bro.find_elements_by_xpath('//button[@name = "saveToExcel"]')[0].click()
                print("index:",i,"sample_index:",j,"  done!")
                sleep(7)
                bro.find_elements_by_xpath('//button[@class="standard-button secondary-button snowplow-wos-markedlist-clear-click"]')[0].click()
                # sleep(2)
                bro.switch_to.alert.accept()
                sleep(1)
                if int(re.findall("\d+", bro.find_elements_by_xpath('//div[@class="NEWpageTitle"]')[0].text)[0]) != 0:
                    bro.find_elements_by_xpath('//button[@class="standard-button secondary-button snowplow-wos-markedlist-clear-click"]')[0].click()
                    bro.switch_to.alert.accept()
                sleep(1)
                bro.quit()
print("all done!!")


#  1.0版本（存在网络慢，复选框更新不出来的问题）
# df=pd.read_csv('./-2_links.csv')   #读取top、median、bottom各十篇对照的url
# for i in range(0,df.shape[0]):      #行，从第0行开始，若因为网络原因中途退出，修改范围接着跑
#     for j in range(1,df.shape[1]):  #列，从第1列开始
#         url=df.iloc[i,j]
#         bro = webdriver.Chrome(executable_path='./chromedriver')
#         bro.get(url)
#         tree=etree.HTML(bro.page_source)
#         if "0" in bro.find_elements_by_xpath('//h2')[0].get_attribute('textContent'):
#             print("index:",i,"sample_index:",j,"no reference!")
#             bro.quit()
#         else:
#             ref=tree.xpath('//a[@class="view-all-link snowplow-view-all-in-cited-references-page-top"]')
#             ref_url = "https://apps.webofknowledge.com//"+str(ref[0].xpath('./@href')[0])
#             bro.get(ref_url)
#             flag=0
#             while int(bro.find_element_by_xpath("//input[@class='goToPageNumber-input']").get_attribute("value")) < int(bro.find_elements_by_xpath('//span[@id= "pageCount.top"]')[0].get_attribute('textContent')):
#                 if "display: none" not in bro.find_element_by_xpath('//div[@class="displayTopBar"]').get_attribute("style"):
#                 #.isDisplayed()也可以判断元素是否隐藏
#                     bro.find_elements_by_xpath('//input[@class="SelectPageChk"]')[0].click()
#                     flag=1
#                     bro.find_elements_by_xpath('//a[@class="paginationNext snowplow-navigation-nextpage-top"]')[0].click()
#                 else:
#                     bro.find_elements_by_xpath('//a[@class="paginationNext snowplow-navigation-nextpage-top"]')[0].click()
#
#             if int(bro.find_element_by_xpath("//input[@class='goToPageNumber-input']").get_attribute("value"))== int(bro.find_elements_by_xpath('//span[@id= "pageCount.top"]')[0].get_attribute('textContent')):
#                 if "display: none" not in bro.find_element_by_xpath('//div[@class="displayTopBar"]').get_attribute("style"):
#                     bro.find_elements_by_xpath('//input[@class="SelectPageChk"]')[0].click()
#                 else:
#                     if flag==0:
#                         print("index:",i,"sample_index:",j,"no reference!")
#                         bro.quit()
#                         continue
#
#             # 一系列自动化点击，完成文件下载
#             bro.find_elements_by_xpath('//a[@title="标记结果列表"]')[0].click()
#             # bro.find_elements_by_xpath('//button[@class="onload-secondary-button exportIconButton nav-link"]')[0].click()
#             # bro.find_elements_by_xpath('//a[@title="将所选记录导出至制表符分隔文件、其他参考文件软件等"]')[0].click()
#             # bro.find_elements_by_xpath('//span[@id="select2-saveOptions-container"]')[0].click()
#             # bro.find_elements_by_xpath('//li[contains(text(), "纯文本")]')[0].click()
#             bro.find_elements_by_xpath('//button[@title="将所选记录导出至制表符分隔文件、其他参考文件软件等"]')[0].click()
#             bro.find_elements_by_xpath('//button[@id="exportButton"]')[0].click()
#             print("index:",i,"sample_index:",j,"  done!")
#             sleep(5)
#             bro.find_elements_by_xpath('//button[@class="standard-button secondary-button snowplow-wos-markedlist-clear-click"]')[0].click()
#             sleep(2)
#             bro.switch_to.alert.accept()
#             sleep(1)
#             bro.quit()
# print("all done!!")
#







