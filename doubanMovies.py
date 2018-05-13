#-------------------------------------------------------------------------------
# Name:        豆瓣-肖申克的救赎
# Created:     05/12/2018
# coding:       utf-8
#-------------------------------------------------------------------------------


import requests
from lxml import etree
'''import sys'''
import json#解决列表或字典输出中文

'''
#sys无法解决中文输出
reload(sys)
sys.setdefaultencoding('utf8')
'''

#获得网页数据
url = 'https://movie.douban.com/subject/1292052/'
data = requests.get(url).text
s  = etree.HTML(data)

#获取元素的xpath信息，存放在列表
film = s.xpath('//*[@id="content"]/h1/span[1]/text()')
rating = s.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
director = s.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
writers = s.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
actors = s.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')
time = s.xpath('//*[@id="info"]/span[13]/text()')

#以打印数据，以中文显示
print "电影名字:",json.dumps(film[0],encoding="utf-8",ensure_ascii=False),
print "豆瓣评分：",rating[0]
print "导演：",json.dumps(director,encoding="utf-8",ensure_ascii=False)
print "编剧：",json.dumps(writers,encoding="utf-8",ensure_ascii=False)
print "主演：",json.dumps(actors[0:4],encoding="utf-8",ensure_ascii=False)
print "时长：",json.dumps(time,encoding="utf-8",ensure_ascii=False)

