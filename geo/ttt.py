#coding=utf-8

import time
from selenium import webdriver
from splinter import Browser


# driver=webdriver.Firefox()
# driver.get("http://geo.ckcest.cn/")
# print(dir(driver))
# remotelist=[1,2,3,4,5,6]
# print("====" + str(len(remotelist)))
# for i in range(0,len(remotelist)):
#     print(i)

####### Browser 功能测试

def testBrowser(url):
    br=Browser('firefox', headless=True)
    # open a url
    br.visit(url)
    #wait for a moment
    time.sleep(3)
    # br.screenshot("D:/csdn", ".png", True)
    br.execute_script('alert("Hello World")')
    br.screenshot("D:/baidu.png")
    br.quit()
    #find a link and click
    # br.find_by_text('账号登录').click()
    # time.sleep(2)
    # #find username input and fill
    # br.find_by_id('username').fill('xxxx')
    # #find password input and fill
    # br.find_by_id('password').fill('xxxx')
    # # find login button and click
    # br.find_by_css('input.logging').click()
    # time.sleep(2)
    # #find a link by text and click
    # br.find_by_text('以后再说').click()
    # time.sleep(2)
    # papertitle = br.find_by_css('ul.feedlist_mod >li > div > div.title >h2 > a')
    # if len(papertitle) > 0:
    #     for title in papertitle:
    #         print(title.html)
    #         print('####################################')
    #
    # #imitate mouse scroll down



# testBrowser('https://passport.csdn.net/account/login')
# testBrowser('https://www.baidu.com/')

pp = ['11','22']
pp2 = ['33','44']
tmp = [val for val in pp if not val in pp2]
tt = set(pp).union(set(pp2))
print(tt)
for x in tt:
    print(x)