# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:33:16 2018

"""

import time
from splinter import Browser
from selenium import webdriver  
browser = Browser()

url='http://geo.ckcest.cn/'
browser.visit(url) 
#人工登陆

#文献下载#文献下载
browser.visit('http://geo.ckcest.cn/scientific/literature/techdoc_v.html') 
#然后跳转到一个页码
linkspage = browser.find_link_by_partial_href('#')
paperurls=[]
for i in range(16,19):
    page=linkspage[i]
    page.click()
    time.sleep(3)
    papers = browser.find_link_by_partial_href('techdoc_papers.html')
    browserurl=browser.url    
    for j in range(0,len(papers)):
        papers[j].click()
        time.sleep(3)
        window = browser.windows[1]
        paperurls.append(window.url) 
        window.close()
for i in range(1,len(paperurls)):
    browser.visit(paperurls[i]) 
    browser.find_by_id('downloadpape').click()
    time.sleep(15)
    window = browser.windows[1]
    browser.visit(window.url)
    window.close()
    browser.find_by_id('keyClick').click()

#图书专著
driver=webdriver.Firefox()
driver.get('http://geo.ckcest.cn/scientific/literature/books.html')  
time.sleep(3)    
papers=driver.find_elements_by_xpath("//*[@href]")  
paperurls=[]
for paper in papers:
    link=paper.get_attribute('href')
    if 'books_bs.html' in link:
        paperurls.append(link)
driver.quit()  
browser.visit('http://geo.ckcest.cn/scientific/literature/books.html') 
time.sleep(3)
for i in range(0,len(paperurls)):
    browser.visit(paperurls[i]) 
    browser.find_by_id('keyFullPaper').click()
    time.sleep(5)
    window = browser.windows[1]
    window.close()  

#考察报告
browser.visit('http://geo.ckcest.cn/scientific/literature/surveyreport/index.html') 
#然后跳转到一个页码
time.sleep(3)
papers = browser.find_link_by_partial_href('datadetails.html') 
paperurls=[]  
for j in range(0,len(papers)):
    papers[j].click()
    time.sleep(3)
    window = browser.windows[1]
    paperurls.append(window.url) 
    window.close()
for i in range(1,len(paperurls)):
    browser.visit(paperurls[i]) 
    browser.find_by_id('dkeyFullPaper').click()
    time.sleep(5)
    window = browser.windows[1]
    window.close()

#遥感影像
browser.visit('http://geo.ckcest.cn/scientific/InternationalData/list.html') 
#然后跳转到一个页码
linkspage = browser.find_link_by_partial_href('#')
paperurls=[]
for i in range(11,12):#(10,15)
    page=linkspage[i]
    page.click()
    time.sleep(8)
    papers = browser.find_link_by_partial_href('remotedetail.html')
    browserurl=browser.url    
    for j in range(0,len(papers)):#len(papers)
        papers[j].click()
        time.sleep(8)
        window = browser.windows[1]
        paperurls.append(window.url) 
        window.close()
for i in range(1,len(papers)):
    browser.visit(paperurls[i]) 
    time.sleep(5)
    remotelist=browser.find_by_id('remotelist')
    within_elements = remotelist.first.find_by_tag('a')
    for j in range(0,len(within_elements)):
        within_elements[j].click()
        time.sleep(5)
browser.windows[0].close()

