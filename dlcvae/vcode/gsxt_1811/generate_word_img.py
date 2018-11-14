# -*- coding: utf-8 -*-

import os
import pygame
import io

from PIL import Image


def yStart(grey):
    m,n = grey.size
    for j in range(n):
        for i in range(m):
            if grey.getpixel((i,j)) == 0:
                return j
def yEnd(grey):
    m,n = grey.size
    for j in range(n-1,-1,-1):
        for i in range(m):
            if grey.getpixel((i,j)) == 0:
                return j

def xStart(grey):
    m,n = grey.size
    for i in range(m):
        for j in range(n):
            if grey.getpixel((i,j)) == 0:
                return i
def xEnd(grey):
    m,n = grey.size
    for i in range(m-1,-1,-1):
        for j in range(n):
            if grey.getpixel((i,j)) == 0:
                return i
def xBlank(grey):
    m,n = grey.size
    blanks = []
    for i in range(m):
        for j in range(n):
            if grey.getpixel((i,j)) == 0:
                break
        if j == n-1:
            blanks.append(i)
    return blanks

def yBlank(grey):
    m,n = grey.size
    blanks = []
    for j in range(n):
        for i in range(m):
            if grey.getpixel((i,j)) == 0:
                break
        if i == m-1:
            blanks.append(j)
    return blanks

def getWordsList():
    f = open('3500.txt')
    line = f.read().strip()
    wordslist = line.split(' ')
    f.close()
    return wordslist

count = 0
wordslist = []
def getWordsByBlank(img,path):
    '''根据行列的空白取图片，效果不错'''
    global count
    global wordslist
    grey = img.split()[0]
    xblank = xBlank(grey)
    yblank = yBlank(grey)
    #连续的空白像素可能不止一个，但我们只保留连续区域的第一个空白像素和最后一个空白像素，作为文字的起点和终点
    xblank = [xblank[i] for i in range(len(xblank)) if i == 0 or i == len(xblank)-1 or not (xblank[i]==xblank[i-1]+1 and xblank[i]==xblank[i+1]-1)]
    yblank = [yblank[i] for i in range(len(yblank)) if i == 0 or i == len(yblank)-1 or not (yblank[i]==yblank[i-1]+1 and yblank[i]==yblank[i+1]-1)]
    for j in range(len(yblank)/2):
        for i in range(len(xblank)/2):
            area = (xblank[i*2],yblank[j*2],xblank[i*2+1]+32,yblank[j*2]+32)#这里固定字的大小是32个像素
            #area = (xblank[i*2],yblank[j*2],xblank[i*2+1],yblank[j*2+1])
            word = img.crop(area)
            word.save(path+wordslist[count]+'.png')
            count += 1
            if count >= len(wordslist):
                return


def getWordsFormImg(imgName,path):
    png = Image.open(imgName,'r')
    img = png.convert('1')
    grey = img.split()[0]
    #先剪出文字区域
    area = (xStart(grey)-1,yStart(grey)-1,xEnd(grey)+2,yEnd(grey)+2)
    img = img.crop(area)
    getWordsByBlank(img,path)

def getWrods():
    global wordslist
    wordslist = getWordsList()
    imgs = ["l1.png","l2.png","l3.png"]
    for img in imgs:
        getWordsFormImg(img,'words/')

##########生成文字
def pasteWord(word):
    '''输入一个文字，输出一张包含该文字的图片'''
    pygame.init()
    font = pygame.font.Font(os.path.join("./fonts", "a.ttf"), 22)
    im = Image.new("RGB", (300, 50), (255, 255, 255))
    # text = word.decode('utf-8')
    # imgName = "D:/chinese/"+text+".png"
    # paste(text,font,imgName)
    rtext = font.render(word, True, (0, 0, 0), (255,255,255))
    sio = io.StringIO()
    pygame.image.save(rtext, sio)
    sio.seek(0)
    line = Image.open(sio)
    im.paste(line, (10,5))
    im.show()
    im.save("t.png")


def paste(text,font,imgName,area = (0, -9)):
    '''根据字体，将一个文字黏贴到图片上，并保存'''
    im = Image.new("RGB", (32, 32), (255, 255, 255))
    rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
    sio = io.StringIO()
    pygame.image.save(rtext, sio)
    sio.seek(0)
    line = Image.open(sio)
    im.paste(line, area)
    #im.show()
    im.save(imgName)

if __name__ == "__main__":
    # getWrods()
    word = '你好'
    pasteWord(word)