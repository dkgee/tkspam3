# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:33:16 2018

@author: JIANGHOU
"""

import time
from splinter import Browser
from selenium import webdriver
browser = Browser()

url='http://geo.ckcest.cn/'
browser.visit(url)
#人工登陆

#遥感影像
browser.visit('http://geo.ckcest.cn/scientific/InternationalData/list.html')
#然后跳转到一个页码
linkspage = browser.find_link_by_partial_href('#')
paperurls=[]
time.sleep(3)
papers = browser.find_link_by_partial_href('remotedetail.html')
browserurl=browser.url
for j in range(0,10):#len(papers)
    papers[j].click()
    time.sleep(3)
    window = browser.windows[1]
    paperurls.append(window.url)
    window.close()
for i in range(1,10):
    browser.visit(paperurls[i])
    time.sleep(15)
    remotelist=browser.find_by_id('remotelist')
    within_elements = remotelist.first.find_by_tag('a')
    for j in range(1,len(within_elements)):
        within_elements[j].click()
        time.sleep(5)
browser.windows[0].close()


#144 76 30 655 905