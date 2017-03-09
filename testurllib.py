# coding:utf-8
import urllib.request

def print_list(list):
    for l in list:
        print(l)

def print_process(block_size, block_num, total_size):
    print("block_size:%d,total_size:%d,%.02f%%"% (block_size*block_num, total_size, (float)(block_size*block_num)*100/total_size))

def demo():
    s = urllib.request.urlopen('http://www.baidu.com')
#    list = s.readlines()
#    print_list(list)
 #   code = s.getcode()
 #   print(code)
 #   print(s.close())
    msg = s.info()
#    print_list(dir(msg))
#    items = msg.items()
#    print_list(items)


    filename, msg = urllib.request.urlretrieve('http://www.cnblogs.com/sysu-blackbear/p/3629420.html','index.html', reporthook=print_process)
    print(filename)
    print(msg._headers)

from urllib.parse import urlparse, urlencode, parse_qs
def urlcodedemo():
    user = {'name':'cityking', 'host':'127.0.0.1','port':'8000','name_cn':'王城'}
    urlcode = urlencode(user)
    print(urlcode)
    code_qs = parse_qs(urlcode)
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E7%88%AC%E8%99%AB&oq=python%2526lt%253B%2520urlencode&rsv_pq=bbcc2ea600094403&rsv_t=6d9fFm6EV7aS77cEUr8WMahXEpBU9uLoDP26FCPzDkV3EMWGrpkHf9Sif7k&rqlang=cn&rsv_enter=1&inputT=14880&rsv_sug3=82&rsv_sug1=84&rsv_sug7=100&bs=python3%20urlencode'
    result = urlparse(url)
    print(result)
    param = parse_qs(result.query)
    print(param)
    print(code_qs)


if __name__ == '__main__':
    urlcodedemo()
