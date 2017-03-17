# coding:utf-8

import re
import requests
from html.parser import HTMLParser

class PoemParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tangshi_list = []
        self.current_poem = {}
        self.in_div = False
        self.in_span = False
        self.in_a = False
    def handle_starttag(self, tag, attrs):
        if tag=='div' and _attr(attrs, 'class')=='son2':
            self.in_div = True
        if self.in_div and tag=='span':
            self.in_span = True
        if self.in_span and tag=='a':
            self.in_a = True
            self.current_poem['url'] = _attr(attrs, 'href')

    def handle_endtag(self, tag):
        if tag == 'div':
            self.in_div = False
        if tag == 'span':
            self.in_span = False
        if tag == 'a':
            self.in_a = False

    def handle_data(self, data):
        if self.in_span:
            if self.in_a:
                self.current_poem['title'] = data
            else:
                if re.match(r'\((.*)\)', data):
                    data = re.match(r'\((.*)\)', data).group(1)
                    self.current_poem['author'] = data
                    self.tangshi_list.append(self.current_poem)
                    self.current_poem = {}


class PoemContentParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = [] 
        self.in_div = False
    def handle_starttag(self, tag, attrs):
        if tag=='div' and _attr(attrs, 'id')=='cont':
            self.in_div = True
    def handle_endtag(self, tag):
        if tag=='div':
            self.in_div=False
    def handle_data(self, data):
        if self.in_div:
            self.content.append(data)

        

def _attr(attrs, attrname):        
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None


def retrive_tangshi_300():
    url = 'http://so.gushiwen.org/gushi/tangshi.aspx'
    r = requests.get(url)
    parser = PoemParser() 
    parser.feed(r.text)
    return parser.tangshi_list

def download_poem(current_poem):
    poem = {}
    poem['title'] = current_poem['title']
    poem['author'] = current_poem['author']
    url = 'http://so.gushiwen.org' + current_poem['url']
    r = requests.get(url)
    parser = PoemContentParser()
    parser.feed(r.text)
    poem['content'] = '\n'.join(parser.content)
    return poem


if __name__ == '__main__':
    l = retrive_tangshi_300()
    for i in range(10):
        poem = download_poem(l[i])
        print("标题：%s   作者：%s" % (poem['title'], poem['author']))
        print(poem['content'])
