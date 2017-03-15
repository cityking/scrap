import requests
from html.parser import HTMLParser

def _attr(attrs, attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None

def _get_ck(content):
    class CKParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck = None
        def handle_starttag(self, tag, attrs):
            if tag=='input' and _attr(attrs, 'type')=='hidden' and _attr(attrs, 'name')=='ck':
                self.ck = _attr(attrs, 'value')
    p = CKParser()
    p.feed(content)
    return p.ck

def _get_captcha(content):
    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.captcha_id = None
            self.captcha_url = None
        def handle_starttag(self, tag, attrs):
            if tag=='img' and _attr(attrs, 'id')=='captcha_image' and _attr(attrs, 'class')=='captcha_image':
                self.captcha_url = _attr(attrs, 'src')
            if tag=='input' and _attr(attrs, 'type')=='hidden' and _attr(attrs, 'name')=='captcha-id':
                self.captcha_id = _attr(attrs, 'value')
    parser = CaptchaParser()
    parser.feed(content)
    return parser.captcha_id, parser.captcha_url

class DoubanClient(object):
    def __init__(self):
        object.__init__(self)
        self.session = requests.Session()

    def login(self, username, password, source=None, redir='https://www.douban.com/people/52179393/', login='登录'):
        url = 'https://www.douban.com/accounts/login'
        headers = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36', 
                'host':'www.douban.com',
                }
        r = self.session.get(url, headers=headers)
        data = {
                'form_email':username,
                'form_password':password,
                'source': source,
                'redir':redir,
                'login':login,
                }
        (captcha_id, captcha_url) = _get_captcha(r.text)
        if captcha_id:
            captcha_solution = input('please input solution for [%s]:' % captcha_url)
            data['captcha-id'] = captcha_id
            data['captcha-solution'] = captcha_solution
        print(data)
        headers = {
                'referer':'https://www.douban.com/accounts/login',
                'host':'accounts.douban.com',
                'origin':'https://www.douban.com',
                }
        url = 'https://accounts.douban.com/login'
        self.session.post(url, data=data, headers=headers)
        print(self.session.cookies.items())
    def edit_signature(self, signature):
        url = 'https://www.douban.com/people/52179393' 
        r = self.session.get(url)
        ck = _get_ck(r.text)
        data = {'signature':signature, 'ck':ck} 
        headers = {
                'referer':'https://www.douban.com/people/52179393/', 
                'host':'www.douban.com',
                'x-requested-with':'XMLHttpRequest',
                }
        url = 'https://www.douban.com/j/people/52179393/edit_signature'
        r = self.session.post(url,headers=headers, data=data)
        print(r.text)


if __name__ == '__main__':
    c = DoubanClient()
    c.login('18221339272', 'ct065410')
    c.edit_signature('work')
