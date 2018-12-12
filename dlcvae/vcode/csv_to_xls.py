# -*- coding: utf-8 -*-
# py-version: Python 3.7
# requirement: csv、openpyxl
# description：将csv文件导出至Excel保存，每超过65536行，新建一个sheet保存
# author: jht
# date: 2018-12-12 09:34

import csv
from openpyxl import Workbook

csv_file_path = "D:/bootleg.csv"        # csv文件保存路径
xls_file_path = "D:/target.xlsx"        # Excel文件保存路径
sheet_max_number = 65536                # Excel每一个Sheet最大条数

with open(csv_file_path, "r") as csvfile:
    read = csv.reader(csvfile)
    workbook = Workbook()
    x = 1
    page = 1
    sheet = workbook.active
    sheet.title = str(page)
    print("First sheet:" + str(x))
    for i in read:
        if x > sheet_max_number:
            page += 1
            sheet = workbook.create_sheet(str(page), index=0)
            print("Create new sheet:" + str(page))
            x = 1
        else:
            x += 1
            sheet.append(i)
    workbook.save(xls_file_path)
