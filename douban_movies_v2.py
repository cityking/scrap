# coding: utf-8    
import requests 
from html.parser import HTMLParser

class MovieParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies=[]
        self.in_movie = False

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
            self.in_movie = True
        if tag=='img' and self.in_movie:
            movie = self.movies[-1]
            movie['img-url']=_attr(attrs, 'src')
            _download_movie_img(movie)
            self.in_movie=False

def nowplaying_movies(url):
    headers = {'User-Agent':'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    parser = MovieParser()
    parser.feed(r.text)
    


    return parser.movies

def _download_movie_img(movie):
    url = movie['img-url']
    r = requests.get(url)
    filename = url.split('/')[-1]
    with open(filename, 'wb') as f:
        f.write(r.content)
        movie['img-name']=filename
if __name__ == "__main__":
    url = 'https://movie.douban.com/nowplaying/chengdu/'
    movies = nowplaying_movies(url)
    for movie in movies:
        print("%s | %s | %s | %s | %s" % (movie['title'], movie['director'], movie['actors'], movie['score'], movie['img-name']))

