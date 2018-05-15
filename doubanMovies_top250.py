#-------------------------------------------------------------------------------
# Name:        豆瓣电影-top250
# Created:     05/15/2018
# coding:       utf-8
#-------------------------------------------------------------------------------


import requests
from lxml import etree
import sys
import json#解决列表或字典输出中文


#sys无法解决中文输出
reload(sys)
sys.setdefaultencoding('utf8')


#爬取第几页面的数据,page每25为一页
def pagedata(page):
    #获得网页数据
    url = 'https://movie.douban.com/top250?start=%d&filter=' % page
    data = requests.get(url).text
    s = etree.HTML(data)

    #获取元素的xpath信息，存放在列表。网址前面相同的部份,确保获取到列表信息无论多少，仍能在输出时匹配
    file = s.xpath('//*[@id="content"]/div/div[1]/ol/li/div')
    for div in file:
        rank = div.xpath('./div[1]/em/text()')[0]
        film = div.xpath('./div[2]/div[1]/a/span[1]/text()')[0]
        text = div.xpath('./div[2]/div[2]/p[1]/text()')[0]
        rating = div.xpath('./div[2]/div[2]/div/span[2]/text()')[0]

        #处理掉信息前面空格，分割成两部分
        text = text.split('\n                            ')

        print u"top250排名：",rank
        print "电影名字:", json.dumps(film, encoding="utf-8", ensure_ascii=False),
        print "豆瓣评分：", rating
        print "资料：", json.dumps(text[1], encoding="utf-8", ensure_ascii=False)#取第2个
        print ''


#获取前10页的数据，top250
number = 0
while number < 11:
    page = number * 25
    pagedata(page)
    number += 1