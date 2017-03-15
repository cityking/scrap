# coding:utf-8
import requests
from html.parser import HTMLParser

#爬取所有分类
class CategoryParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_div = False
        self.in_li = False
        self.in_a = False
        self.categorys = []
        self.category = {}
    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None

        if tag=="div" and _attr(attrs, 'class')=="a-row":
            self.in_div = True
        if self.in_div and tag=='li' and _attr(attrs, 'class')=='a-spacing-small':
            self.in_li = True
        if self.in_li and tag == 'a' and _attr(attrs, 'class')=='nav_a a-link-normal a-color-base':
            self.in_a = True
            self.category['url'] = 'https://www.amazon.cn'+_attr(attrs, 'href')

    def handle_endtag(self, tag):
        if tag=="div":
            self.in_div = False
        if tag == "li":
            self.in_li = False
        if tag == "a":
            self.in_a = False

    def handle_data(self, data):
        if self.in_a:
            self.category['title']=data
            cate = self.category
            self.categorys.append(cate)
            self.category = {}

#爬取商品名称和url
class ItemParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_div = False
        self.in_a = False
        self.items = []
        self.item = {}
    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None

        if tag=="div" and _attr(attrs, 'class')=="a-row a-spacing-none":
         
            self.in_div = True
        if self.in_div and tag == 'a':
            if _attr(attrs, 'class') == 'a-link-normal s-access-detail-page  a-text-normal':
                self.in_a = True
                self.item['url'] = _attr(attrs, 'href')
                self.item['title'] = _attr(attrs, 'title')
                self.items.append(self.item)
                self.item = {}

    def handle_endtag(self, tag):
        if tag=="div":
            self.in_div = False
        if tag == "a":
            self.in_a = False

#爬取商品详细信息
class DetailParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_tr = False
        self.in_td = False
        self.in_span = False
        self.details = []
        self.detail = {}
    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None

        if tag=="tr" and _attr(attrs, 'class')=="priceblock_ourprice_row":
            self.in_tr = True
        if self.in_tr and tag == 'td' and _attr(attrs, 'class') == 'a-span12':
            self.in_td = True
        if self.in_td and tag == 'span' and _attr(attrs, 'class') == 'a-size-medium a-color-price':
            self.in_span = True

    def handle_endtag(self, tag):
        if tag=="tr":
            self.in_tr = False
        if tag == "td":
            self.in_td = False
        if tag == "span":
            self.in_span = False

    def handle_data(self, data):
        if self.in_span:
            self.detail['price'] = data





def scrapy_categorys(url):
    response = requests.get(url)
    parser = CategoryParser()
    parser.feed(response.text)
    return parser.categorys
   

def scrapy_items(category):
    url = category['url']
    response = requests.get(url)
    parser = ItemParser()
    parser.feed(response.text)
    return parser.items

def scrapy_details(item):
    url = item['url']
    response = requests.get(url)
    parser = DetailParser()
    parser.feed(response.text)
    return parser.details


if __name__ == '__main__':
    url = 'https://www.amazon.cn/gp/site-directory/ref=nav_shopall_btn' 
    categorys = scrapy_categorys(url)
    for category in categorys: 
        items = scrapy_items(category)
        if len(items) != 0:
            for item in items:
                print(item)
