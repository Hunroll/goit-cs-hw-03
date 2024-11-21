from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import secret
from cat import Cat, cat_features
from faker import Faker
import random

def connect():
    try:
        uri = secret.dbConn
        client = MongoClient(uri, server_api=ServerApi('1'))
        return client.book
    except Exception as e:
        print("Error connecting to DB!")
        print(e)
        return None

def create(db, cat: Cat):
    db.cats.insert_one({
        "name": cat.name,
        "age": cat.age,
        "features": cat.features
    })

def read_all(db) -> []:
    '''Реалізуйте функцію для виведення всіх записів із колекції.'''
    result = db.cats.find({})
    result = [Cat(el["name"], el["age"], el["features"]) for el in result]
    return result

def read_one(db, cat_name) -> Cat:
    '''Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.'''
    el = db.cats.find_one({"name":cat_name})
    if el:
        result = Cat(el["name"], el["age"], el["features"])
    else:
        result = None
    return result

def update_age(db, cat_name, age) -> Cat:
    '''Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.'''
    db.cats.update_one({"name": cat_name}, {"$set": {"age": age}})

    el = db.cats.find_one({"name":cat_name})
    if el:
        result = Cat(el["name"], el["age"], el["features"])
    else:
        result = None
    return result

def add_feature(db, cat_name, new_feature) -> Cat:
    '''Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям
    [Нова характеристика кота буде додана саме до списку, не до множини (сета), тому можливі повторювання]'''
    el = db.cats.find_one({"name":cat_name})
    if el:
        cat = Cat(el["name"], el["age"], el["features"])
    else:
        return None
    
    cat.features.append(new_feature)
    db.cats.update_one({"name": cat_name}, {"$set": {"features": cat.features}})

    el = db.cats.find_one({"name":cat_name})
    return Cat(el["name"], el["age"], el["features"])

def delete_one(db, cat_name) -> bool:
    '''Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.'''
    el = db.cats.find_one({"name":cat_name})
    if not el:
        return False
    
    try:
        db.cats.delete_one({"name": cat_name})
        res = True
    except:
        res = False
    return res

def delete_all(db):
    '''Реалізуйте функцію для видалення всіх записів із колекції.'''
    db.cats.delete_many({})

def generate_random_cats(db, count: int):
    f = Faker()
    for _ in range(count):
        features = set()
        for _ in range(random.randint(1, 3)):
            features.add(cat_features[random.randint(0, len(cat_features) - 1)])
        cat = Cat(f.name(), random.randint(1, 10), list(features))
        create(db, cat)

def main():
    db = connect()
    if db is None:
        print('DB is not defined')
        return


    generate_random_cats(db, 10)


    print('Вичитка всіх котів')
    print('\n'.join([str(cat) for cat in read_all(db)]))
    print()
    

    print('Вичитка одного кота')
    cat_name = input('Введіть ім\'я кота >> ')
    cat = read_one(db, cat_name)
    print(cat if cat else f'Кота "{cat_name}" не знайдено')
    print()


    print('Оновлення віку кота')
    cat_name = input('Введіть ім\'я кота >> ')
    while True:
        try:
            cat_age = int(input('Введіть вік кота >> '))
            break
        except ValueError:
            print('Неправильно введено вік')
    cat = update_age(db, cat_name, cat_age)
    print(cat if cat else f'Кота "{cat_name}" не знайдено')
    print()


    print('Додавання нової характеристики')
    cat_name = input('Введіть ім\'я кота >> ')
    cat_feature = input('Введіть нову характеристику кота >> ')
    cat = add_feature(db, cat_name, cat_feature)
    print(cat if cat else f'Кота "{cat_name}" не знайдено')
    print()


    print('Видалення зі списку одного кота') 
    cat_name = input('Введіть ім\'я кота >> ')
    delete_result = delete_one(db, cat_name)
    print(f'Кота {cat_name} {"видалено" if delete_result else "не знайдено/не видалено"}')
    print()


    print('Видалення всіх котів')
    delete_all(db)
    print('Котів видалено.')
    print(f'Залишилось {len(read_all(db))} котів')

    
if __name__ == "__main__":
    main()