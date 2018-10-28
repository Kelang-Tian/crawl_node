from conn_client import ClientConnection
import socket
import json
import time
from bs4 import BeautifulSoup
import requests
from lxml import etree

"""
def getinfo(newsURL, path1, path2, attr):
    html = gethtmltext(newsURL)
    try:
        soup = BeautifulSoup(html, 'html.parser')
        info = soup.find(path1, attrs={path2: attr})
        return info
    except:
        return ""
"""


def gethtmltext(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except requests.exceptions.ConnectionError:
        return ""


def getinfo(url,xpaths):
    text = gethtmltext(url)
    try:
        html = etree.HTML(text)
        title = html.xpath(xpaths["title"])
        data = html.xpath(xpaths["data"])
        source = html.xpath(xpaths["source"])
        artical = html.xpath(xpaths["artical"])
        news_url = html.xpath(xpaths["news_url"])

        list = list()
        list.append(title)
        list.append(data)
        list.append(source)
        list.append(artical)
        list.append(news_url)
        return list
    except:
        return ""


while True:
    try:

        #客户端链接
        client = ClientConnection()
        client.connect()
        #获取url
        url = client.request_tasks()
        xpaths = client.request_xpath("finance.sina.com")

        #信息解析
        data = getinfo(url, xpaths)
        client.submit_data(data)

    except ConnectionError:
        print("Connection error.Do nothing")
        time.sleep(5)


