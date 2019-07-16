# -*- coding: utf-8 -*-

import sys
import os
import jieba


# seg_list=jieba.cut("小明1995年毕业于北京清华大学", cut_all=False)
# print("DefaultMode:","".join(seg_list)) #默认切分
#
# seg_list=jieba.cut("小明1995年毕业于北京清华大学")
# print(" ".join(seg_list))
##分析效果比较自然，相比较全切分，比较粗糙

# seg_list=jieba.cut("小明1995年毕业于北京清华大学", cut_all=True)
# print("FullMode:","/".join(seg_list)) #全切分
#
# seg_list=jieba.cut("小明1995年毕业于北京清华大学", cut_all=True)
# print("FullMode:","/".join(seg_list)) #全切分
##分词效果更详细

seg_list=jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") #搜索引擎模式
print("/ ".join(seg_list)) #全切分
##搜索引擎模式切分效果非常不错，一些组合词汇及组合基本词汇均包括