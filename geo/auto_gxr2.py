# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:33:16 2018

"""
#

import time
from splinter import Browser
from selenium import webdriver

class Geo:

	# 输出用户名 xxxx
	# 输入密码   xxxxx
	# 验证码	xxxx
	def login(self):
		print("》》》》》》》》》》》》》》首页开始登录(您有 20s 时间输入用户名、密码、验证码).....")
		self.driver=Browser("firefox")
		br=self.driver
		br.visit("http://geo.ckcest.cn/")
		time.sleep(20)
		print("》》》》》》》》》》》》》》登录完成")


	#遥感影像
	def remoteImage(self):
		print("》》》》》》》》》》》》》》开始遥感影像下载")
		br=self.driver
		br.visit('http://geo.ckcest.cn/scientific/InternationalData/list.html')
		time.sleep(5)
		linkspage = br.find_link_by_partial_href('remotedetail.html')
		pictureurls=[]
		for i in range(0,len(linkspage)):
			linkpage=linkspage[i]
			txt=linkpage.html
			if txt != '查看数据':
				linkpage.click()
				time.sleep(2)
				window = br.windows[1]
				if window.url.startswith('http://'):
					pictureurls.append(window.url)
				window.close()
		print("》》》》》》》》》》》》》》遥感影像下载地址获取完成")
		browser=self.driver
		for i in range(1,len(pictureurls)):
			browser.visit(pictureurls[i])
			time.sleep(5)
			remotelist=browser.find_by_id('remotelist')
			within_elements = remotelist.first.find_by_tag('a')
			for j in range(0,len(within_elements)):
				within_elements[j].click()
				time.sleep(5)
		browser.windows[0].close()
		print("》》》》》》》》》》》》》》遥感影像文件下载完成.")

	def book(self):
		print("》》》》》》》》》》》》》》开始查看图书专著")
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
		browser=self.driver
		browser.visit('http://geo.ckcest.cn/scientific/literature/books.html')
		time.sleep(3)
		for i in range(0,len(paperurls)):
			browser.visit(paperurls[i])
			pp=browser.find_by_id('keyFullPaper')
			if len(pp) > 0:
				pp.first.click()
				time.sleep(5)
			window = browser.windows[1]
			window.close()
		print("》》》》》》》》》》》》》》图书专著查看完成")

	def surveyreport(self):
		print("》》》》》》》》》》》》》》开始查看考察报告")
		browser=self.driver
		browser.visit('http://geo.ckcest.cn/scientific/literature/surveyreport/index.html')
		#然后跳转到一个页码
		time.sleep(3)
		papers = browser.find_link_by_partial_href('datadetails.html')
		paperurls=[]
		for j in range(0,len(papers)):
			papers[j].click()
			time.sleep(3)
			window = browser.windows[1]
			if window.url.startswith('http://'):
				paperurls.append(window.url)
			window.close()
		for i in range(1,len(paperurls)):
			browser.visit(paperurls[i])
			pp=browser.find_by_id('keyFullPaper')
			if len(pp) > 0:
				pp.first.click()
				time.sleep(5)
			window = browser.windows[1]
			window.close()
		print("》》》》》》》》》》》》》》考察报告查看完成")

	def close(self):
		print("》》》》》》》》》》》》》》关闭浏览器")
		self.driver.windows[0].close()

###########################################################
geo=Geo()
#用户登录
geo.login()
#遥感影像
geo.remoteImage()
#图书专著
#geo.book()
#考察报告
#geo.surveyreport()
#关闭浏览器
geo.close()
