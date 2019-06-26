from app.libs.http_s import HTTP
from flask import current_app


# 根据搜索关键字或isbn  通过封装后的requests 进行http请求外部api
class YuShuBook:
    isbn_url = 'https://api.douban.com/v2/book/isbn/{}'
    keyword_url = 'https://api.douban.com/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)  # 链式查找 可以找到类变量isbn_url
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        # print('page {}'.format(page))
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)


    def __fill_collection(self, data):
            self.total = data['total']
            self.books = data['books']


    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if self.total >=1 else None
# https://api.douban.com/v2/book/isbn/9787308083256