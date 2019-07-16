# -*- coding: utf-8 -*-

from lxml import html

path = "D:\\test\\dream.html"
content = open(path, "rb").read()
page = html.document_fromstring(content)    #解析文件
text = page.text_content()  #去除所有标签
print(text)