#!usr/bin/python3
import requests
from pyquery import PyQuery
import os
import time
import json


class Model(object):
    """打印显示类属性的信息"""

    def __repr__(self):
        name = self.__class__.__name__
        properties = (f'{k}=({v})' for k, v in self.__dict__.items())
        string = '\n '.join(properties)
        s = f'\n<{name} \n {string}>'
        return s


class Movie(Model):
    def __init__(self):
        self.name = ''
        self.rating = ''
        self.quote = ''
        self.img_url = ''
        self.people = ''
        self.rank = ''


def cached_page(url):
    """下载页面，写入cached目录内"""
    folder = 'cached'
    filename = url.split('=', 1)[-1] + ".html"
    path = os.path.join(folder, filename)
    # 存在已下载的文件，则打开返回二进制只读结果
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    # 不存在，是新资源，创建
    else:
        # 不存在cached目录就创建
        if not os.path.exists(folder):
            os.makedirs(folder)
        # 写入数据
        headers = {
            "User-Agent": """
            Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) 
            AppleWebKit/537.36 (KHTML, like Gecko) 
            Chrome/68.0.3440.106 
            Mobile Safari/537.36
            """
        }
        s = requests.get(url, headers)
        # print(s)
        r = s.content
        # print("s__", s)
        with open(path, "wb") as f:
            f.write(r)
        return r


def get_movie(div):
    e = PyQuery(div)

    m = Movie()
    m.name = e('.title').text().split(' ')[0]
    m.quote = e('.inq').text()
    m.img_url = e('img').attr('src')
    m.rating = e('.rating_num').text()
    m.people = e('.star').find('span').text()[6:]
    m.rank = e('.pic').find('em').text()
    return m


def movies_from_url(url):
    page = cached_page(url)
    # 解析dom
    e = PyQuery(page)
    # 每个class="item"是一部电影
    items = e('.item')
    # print(dir(items))
    s = [get_movie(i) for i in items]
    # print(s)
    return s


def down_img(n, name, url):
    """打开url下载大图,保存为 排名+name.jpg 在img目录"""
    if len(n) == 1:
        n = '00' + n
    elif len(n) == 2:
        n = '0' + n
    else:
        n = n
    name = n + '_' + name + '.jpg'
    folder = 'img'
    path = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)
    if os.path.exists(path):
        return

    headers = {
        "User-Agent": """
        Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) 
        AppleWebKit/537.36 (KHTML, like Gecko) 
        Chrome/68.0.3440.106 
        Mobile Safari/537.36
        """
    }
    s = requests.get(url, headers)
    # print(s)
    r = s.content
    # print("s__", s)
    with open(path, "wb") as f:
        f.write(r)


def save_img(url):
    """获取电影名对应的排名及url"""
    data = movies_from_url(url)
    [down_img(i.rank, i.name, i.img_url) for i in data]


def json_movies(url):
    """保存为'movies.txt'的json文件"""
    lists = movies_from_url(url)
    # print(type(l), l)
    # print(dir(lists))

    # 转成字典
    dict_movie = {}
    for d in lists:
        # print(d.rank, d.name)
        d.rank = int(d.rank)
        dict_movie[d.rank] = {
            'name': d.name,
            'rating': d.rating,
            'people': d.people,
            'img': d.img_url,
            'quote': d.quote,
        }
        # 如果遍历到第一的电影就清空movies.txt文件
        if d.rank == 1:
            os.remove('movies.txt')

    # 追加写入json文件
    # print(dict_movie)
    j = json.dumps(dict_movie, indent=2, ensure_ascii=False)
    # print(j)
    with open('movies.txt', 'a', encoding='utf-8') as f:
        f.write(j)


def main():
    for n in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={n}"
        movies_from_url(url)
        json_movies(url)
        save_img(url)
        print(n)
        time.sleep(1)


if __name__ == '__main__':
    main()
