import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publishers(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Publisher - {self.id}:{self.name}'


class Shops(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Shop - {self.id}:{self.name}'


class Books(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=True)

    publisher = relationship(Publishers, backref='book')

    def __str__(self):
        return f'Book - {self.id}:{self.title}'


class Stocks(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=True)
    count = sq.Column(sq.Integer, nullable=True)

    shop = relationship(Shops, backref='stock')
    book = relationship(Books, backref='stock')

    def __str__(self):
        return f'Stock - {self.id}:{self.count}'


class Sales(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=True)
    date_sale = sq.Column(sq.DateTime, nullable=True)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=True)
    count = sq.Column(sq.Integer, nullable=True)

    stock = relationship(Stocks, backref='sale')

    def __str__(self):
        return f'Sales - {self.id}:({self.price}, {self.data_sale}, {self.count})'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

