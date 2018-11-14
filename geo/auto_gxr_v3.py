# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:33:16 2018

"""
#

import time
import geo.cfg as cfg

from splinter import Browser
from pil.lib.geo_predict import crack_captcha

class Geo:

	def __init__(self):
		if cfg.is_headless:
			self.driver=Browser("firefox", headless=True)
		else:
			self.driver=Browser("firefox")
		self.try_times = 0

	def login(self):
		print("》》》》》》》》》》》》》》首页自动登录.....")
		br=self.driver
		br.visit(cfg.index_url)
		br.find_by_id('d-login').first.click()
		self.login_again()

	def login_again(self):
		br=self.driver
		# #username
		br.find_by_id('username').first.fill(cfg.username)
		# #password
		br.find_by_id('password').first.fill(cfg.password)
		# #imgVcode
		vcode = crack_captcha(cfg.captcha_url, br.cookies.all())
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
		br.visit(cfg.international_url)
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
		print("》》》》》》》》》》》》》》遥感影像文件下载完成.")

	def book(self):
		print("》》》》》》》》》》》》》》开始查看图书专著")
		browser=self.driver
		browser.visit(cfg.literature_url)
		time.sleep(3)
		paperurls = []
		paperurl_first =  browser.find_by_css('#DoiAbstract > a')
		first_size = len(paperurl_first)
		if first_size == 0:
			print("获取第一页链接失败，可能页面超时，暂停2s等待")
			time.sleep(2)
			paperurl_first =  browser.find_by_css('#DoiAbstract > a')
		first_size = len(paperurl_first)
		if first_size > 0:
			print("成功获取第一页，%d，条数据，开始获取第二页"%first_size)
			for tag_a in paperurl_first:
				paperurls.append(tag_a['href'])
			browser.find_by_text('下一页').first.click()
			time.sleep(2)
			paperurl_second =  browser.find_by_css('#DoiAbstract > a')
			if len(paperurl_second) > 0:
				print('成功获取第二页图书专著')
				for tag_b in paperurl_second:
					paperurls.append(tag_b['href'])
		print('本次任务共获取%d个图书专著链接，准备查看'%len(paperurls))
		if len(paperurls) > 0:
			for href in paperurls:
				browser.visit(href)
				pp = browser.find_by_id('keyFullPaper')
				if len(pp) > 0:
					pp.first.click()
					time.sleep(6)
					if len(browser.windows) >= 2:
						window = browser.windows[1]
						window.close()
		print("》》》》》》》》》》》》》》图书专著查看完成")

	def surveyreport(self):
		print("》》》》》》》》》》》》》》开始查看考察报告")
		browser=self.driver
		browser.visit(cfg.surveyreport_url)
		time.sleep(3)
		papers_first = browser.find_link_by_partial_href('datadetails.html')
		paperurls=[]
		if len(papers_first) > 0:
			print('第一页获取%d个考察报告,'%len(papers_first))
			for j in papers_first:
				paperurls.append(j['href'])
			browser.find_by_text('下一页').first.click()
			time.sleep(2)
			papers_second = browser.find_link_by_partial_href('datadetails.html')
			if len(papers_second) > 0:
				print('第二页获取%d个考察报告,'%len(papers_second))
				for k in papers_second:
					paperurls.append(k['href'])
		print('本次任务共获取%d个考察报告链接，准备查看'%len(paperurls))
		if len(paperurls) > 0:
			for href in paperurls:
				browser.visit(href)
				pp = browser.find_by_id('keyFullPaper')
				if len(pp) > 0:
					pp.first.click()
					time.sleep(6)
					if len(browser.windows) >= 2:
						window = browser.windows[1]
						window.close()
		print("》》》》》》》》》》》》》》考察报告查看完成")

	def close(self):
		print("本次任务结束,关闭浏览器")
		self.driver.quit()


if __name__ == '__main__':
	geo=Geo()
	geo.login()
	if cfg.international_status:
		geo.remoteImage()
	if cfg.literature_status:
		geo.book()
	if cfg.surveyreport_status:
		geo.surveyreport()
	geo.close()
