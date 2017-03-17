import re

def re_demo():
    s1 = 'this is-re:test'
    s2 = 'the price of this book is $9.90, I have buy 30 sets'

   # print(re.split(r'\W', s1))
   # print(re.findall(r'\w+', s1))
   # print(re.findall(r'\d+\.?\d*', s2))

   # i = re.finditer(r'\d+\.?\d*', s2)
    r = re.compile(r'''
                \d+ #整数部分
                \.? #小数点，可有可无
                \d* #小数部分，可选
                ''' , re.VERBOSE)
    print(re.findall(r, s2))
   # for m in i:
   #     print(m.group())

   # print(re.subn(r'\d+\.?\d*', 'number', s2))
    m = re.match(r'(\w+) (\w+)', s1)
    print(m.group())
    print(m.groups())
    print(re.search(r'(\d)(\d)(\d)\1\2\3','136136').groups())

    s = '137-7434-7721'
    r = re.search(r'\(+86\)?\b(\d{3}-?\d{4}-?\d{4})\b', s)
    print(r.groups())

if __name__ == '__main__':
    re_demo()
