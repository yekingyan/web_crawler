#-------------------------------------------------------------------------------
# Name:        豆瓣电影-top250
# Created:     05/13/2018
# coding:       utf-8
#-------------------------------------------------------------------------------


import requests
from lxml import etree
import sys
import json#解决列表或字典输出中文


#sys无法解决中文输出
reload(sys)
sys.setdefaultencoding('utf8')


#爬取第几页面的数据
def pagedata(page):
#获得网页数据
    url = 'https://movie.douban.com/top250?start=%d&filter=' % page
    data = requests.get(url).text
    s  = etree.HTML(data)

    for i in range(0,25):
        #获取元素的xpath信息，存放在列表
        rank = s.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/em/text()')
        film = s.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
        text = s.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()')
        rating = s.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')

        #处理text的数据，去除空格
        text[2*i+1] = text[2*i+1].split('\n                            ')
        text[2 * i] = text[2 * i].split('\n                            ')

        #以打印数据，以中文显示
        print "top250排名：",rank[i]
        print "电影名字:",json.dumps(film[i],encoding="utf-8",ensure_ascii=False),
        print "豆瓣评分：",rating[i]
        print "资料：",json.dumps(text[2*i:2*i+1],encoding="utf-8",ensure_ascii=False)
        print ''

#获取前10页的数据
number = 0
while number < 11:
    page = number * 25#每25为一页
    pagedata(page)
    number += 1
