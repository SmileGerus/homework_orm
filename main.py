import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publishers, Books, Shops, Stocks, Sales

NAME = 'postgres'
PASSWORD = '159159-Smile'
BASE_NAME = 'homework'
# AttributeError: partially initialized module 'sqlalchemy.util' has no attribute 'preload_module' (most likely due to a circular import)
DSN = f'postgresql://{NAME}:{PASSWORD}@localhost:5432/{BASE_NAME}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json') as data:
    json_data = json.load(data)

for classes in json_data:
    model_dict = {
        'publisher': Publishers,
        'book': Books,
        'shop': Shops,
        'stock': Stocks,
        'sale': Sales,
    }[classes.get('model')]
    session.add(model_dict(id=classes.get('pk'), **classes.get('fields')))
session.commit()


def get_purchases(publisher: str) -> str:

    books = {}

    subq = session.query(Publishers.id).filter(Publishers.name == publisher).subquery()

    for c in session.query(Books.id, Books.title).join(subq, Books.id_publisher == subq.c.id):
        books[c[1]] = c[0]
    print(books)

    for book, id in books.items():
        for c in session.query(Stocks.id, Stocks.id_shop).filter(Stocks.id_book == id, Stocks.count > 0):
            books[book] = list(c)

    books = dict(filter(lambda item: type(item[1]) == list, books.items()))

    for book, id in books.items():
        for c in session.query(Shops.name).filter(Shops.id == books[book][1]):
            books[book][1] = c[0]

    for book, id in books.items():
        for c in session.query(Sales.price, Sales.count, Sales.date_sale).filter(Sales.id_stock == books[book][0]):
            books[book][0] = c[0] * c[1]
            date = str(c[2]).split()[0].split('-')
            books[book].append(f'{date[2]}-{date[1]}-{date[0]}')

    books = dict(filter(lambda item: len(item[1]) == 3, books.items()))

    result = ''

    for book in books.items():
        max_name = max(map(len, books.keys()))
        result += f'{book[0]:<{max_name}}|{book[1][0]:<6}|{book[1][1]:<10}|{book[1][2]:<10}\n'

    return result


def main():
    publisher = input('Введите издателя: ')
    print(get_purchases(publisher))
    session.close()


if __name__ == '__main__':
    main()
