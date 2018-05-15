#-------------------------------------------------------------------------------
# Name:        豆瓣图书-top250
# Created:     05/15/2018
# coding:       utf-8
#-------------------------------------------------------------------------------

from lxml import etree
import requests

i = 0
#def pagedata(page):
#获取网页数据,每25一页
for p in range(0,250,25):
    url = 'https://book.douban.com/top250?start=%d' % p
    data = requests.get(url).text
    s = etree.HTML(data)

    #去掉xpath多匹配出来的tbody
    file = s.xpath('//*[@id="content"]/div/div[1]/div/table')
    #确保输出内容来自同一本书
    for b in file:
        name = b.xpath('./tr/td[2]/div[1]/a/@title')[0]
        href = b.xpath('./tr/td[2]/div[1]/a/@href')[0]
        writer = b.xpath('./tr/td[2]/p[1]/text()')[0]
        rating = b.xpath('./tr/td[2]/div[2]/span[2]/text()')[0]
        #quote = b.xpath('./tr/td[2]/p[2]/span/text()')[0]#遇到无一句话引述的书会报错并停止
        rating = b.xpath('./tr/td[2]/div[2]/span[2]/text()')[0]

        print "第%d本书" % (i+1)
        print "书名：",name,
        print '  ',rating,"分"
        print writer
        #print quote
        print href
        print ''
        i += 1
