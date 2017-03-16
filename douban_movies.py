# coding: utf-8    
import urllib.request
from html.parser import HTMLParser

class MovieParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies=[]

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None
        if tag=='li' and _attr(attrs, 'data-title') and _attr(attrs, 'data-category')=='nowplaying':
            movie = {}
            movie['title'] = _attr(attrs, 'data-title')
            movie['director'] = _attr(attrs, 'data-director')
            movie['actors'] = _attr(attrs, 'data-actors')
            movie['score'] = _attr(attrs, 'data-score')
            self.movies.append(movie)
def nowplaying_movies(url):
    headers = {'User-Agent':'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    s = urllib.request.urlopen(req)
    parser = MovieParser()
    mybytes = s.read()
    mystr = mybytes.decode("utf8")
    parser.feed(mystr)

    s.close()
    return parser.movies


if __name__ == "__main__":
    url = 'https://movie.douban.com/nowplaying/chengdu/'
    movies = nowplaying_movies(url)
    for movie in movies:
        print("%s | %s | %s | %s" % (movie['title'], movie['director'], movie['actors'], movie['score']))

