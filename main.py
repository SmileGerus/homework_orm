import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publishers, Books, Shops, Stocks, Sales

NAME = 'postgres'
PASSWORD = '159159-Smile'
BASE_NAME = 'homework'
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


def get_shops(publisher_id: str) -> str:
    result = session.query(Books.title, Shops.name, Sales.price, Sales.date_sale
                           ).select_from(Shops). \
        join(Stocks, Shops.id == Stocks.id_shop). \
        join(Books, Stocks.id_book == Books.id). \
        join(Publishers, Books.id_publisher == Publishers.id). \
        join(Sales, Stocks.id == Sales.id_stock)

    if publisher_id.isdigit():
        result = result.filter(Publishers.id == publisher_id, Stocks.count > 0).all()
    else:
        result = result.filter(Publishers.name == publisher_id, Stocks.count > 0).all()

    for title, name, price, date_sale in result:
        print(f"{title: <40} | {name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")


def main():
    publisher = input('Введите издателя: ')
    get_shops(publisher)
    session.close()


if __name__ == '__main__':
    main()
