from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    isbn = Column(String(15), nullable=False, unique=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        # 到Gift 表中检索出相应的礼物
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gifts_counts(cls, isbn_list):
        from app.models.gift import Gift
        # 根据传入的一组ISBN，到wish表 计算出某个礼物的wish心愿数量
        # db.session返回的内容由query后面的参数限制 这里是一个包含多个tuple:(count， isbn)的list  我们不直接返回元组 应该统一返回dict
        # 我们也可以用collection模块下的 namedtuple快速建立对象
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        # 包含tuple的list 转化成一个dict
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
