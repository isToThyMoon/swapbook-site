from flask import current_app

from app.models.base import db, Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    isbn = Column(String(15), nullable=False, unique=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        # 到Gift 表中检索出相应的礼物
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组ISBN，到wish表 计算出某个礼物的wish心愿数量
        # db.session返回的内容由query后面的参数限制 这里是一个包含多个tuple:(count， isbn)的list  我们不直接返回元组 应该统一返回dict
        # 我们也可以用collection模块下的 namedtuple快速建立对象
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
                                      Wish.launched == False,
                                      Wish.isbn.in_(isbn_list),
                                      Wish.status == 1).group_by(
                                      Wish.isbn).all()
        # 包含tuple的list 转化成一个dict
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        # 链式调用
        # 主体Query
        # 子函数
        # 触发条件
        recent_gift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        # print('这是recent_gift: {}'.format(type(recent_gift[0])))
        return recent_gift


