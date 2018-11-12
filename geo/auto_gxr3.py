# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:33:16 2018

"""
#

import time
from splinter import Browser
from selenium import webdriver
from pil.lib.geo_predict import crack_captcha

class Geo:

	def __init__(self):
		self.driver=Browser("firefox")		# firefox浏览器
		self.try_times = 0					# 尝试登录次数

	def login(self):
		print("》》》》》》》》》》》》》》首页自动登录.....")
		br=self.driver
		br.visit("http://geo.ckcest.cn/")
		br.find_by_id('d-login').first.click()
		self.login_again()

	def login_again(self):
		br=self.driver
		# #username
		br.find_by_id('username').first.fill('xxxxx')
		# #password
		br.find_by_id('password').first.fill('xxxx')
		# #imgVcode
		vcode = crack_captcha('https://sso.ckcest.cn/portal/captchaCode', br.cookies.all())
		print('识别验证码完成：' + vcode)
		br.find_by_id('imageverifycode').first.fill(vcode)
		br.find_by_css('input.login_button').first.click()
		#msg
		msgs = br.find_by_id('msg')
		if len(msgs) > 0:
			self.try_times += 1
			print('登录失败，验证码错误。')
			if self.try_times <= 5:
				print('第' + str(self.try_times) + '次登录')
				self.login_again()
			else:
				print(str(self.try_times) + '次登录均失败，请手动登录(20s等待用户输入时间)')
				time.sleep(20)
		else:
			print('自动登录成功')

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
# geo.remoteImage()
# #图书专著
geo.book()
# #考察报告
# geo.surveyreport()
# #关闭浏览器
# geo.close()
