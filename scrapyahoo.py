from urllib import parse, request

def download_stock_data(stock_list):
    for sid in stock_list:
        url='http://table.finance.yahoo.com/table.csv?'
        params = {'s':sid+'.sz'}
        url = url+parse.urlencode(params)
        filename = sid+'.sz'
        result = request.urlopen(url)
        code = result.getcode()
        if code==200:
            filename,msg = request.urlretrieve(url, filename)
        print(filename)
        print(msg)
def download_stock_data_in_period(stock_list, start, end):
    for sid in stock_list:
        url='http://table.finance.yahoo.com/table.csv?'
        params = {'s':sid+'.sz', 'a':start.month-1, 'b':start.day, 'c':start.year, 'd':end.month-1, 'e':end.day, 'f':end.year}
        url = url+parse.urlencode(params)
        filename ='%d%d%d%d%d%d%s.sz' % (start.year, start.month-1, start.day, end.year, end.month-1, end.day, sid)
        result = request.urlopen(url)
        code = result.getcode()
        if code==200:
            filename,msg = request.urlretrieve(url, filename)
        print(filename)
        print(msg)


if __name__ == '__main__':
    stock_list = ['000001', '000002']
    import datetime
    start = datetime.date(year=2017, month=2, day=1)
    end = datetime.date(year=2017, month=3, day=1)
    download_stock_data_in_period(stock_list, start, end)
