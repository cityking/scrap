# coding: utf-8

import requests

def get_json():
    r = requests.get('https://api.github.com/events')
    print(r.status_code)
    print(r.headers)
    print(r.content[0:100])
    print('='*80)
    print(r.text[0:100])
#    print(r.json())

def get_querystring():
    url = 'http://httpbin.org/get'
    params = {'qs1':'value1', 'qs2':'value2'}
    r = requests.get(url, params=params)
    print(r.status_code)
    print(r.content)

#定制http头
def get_custom_headers():
    url = 'http://httpbin.org/get'
    headers = {'x-header1':'value1', 'x-header2':'value2'}
    r = requests.get(url, headers=headers)
    print(r.status_code)
    print(r.content)

def get_cookie():
    headers = {'User-Agent':'Chrome'}
    url = 'http://www.douban.com'
    r = requests.get(url, headers=headers)
    print(r.status_code)
    print(r.cookies['bid'])

if __name__ == "__main__":
    #get_json()
    #get_querystring()
    #get_custom_headers()
    get_cookie()

