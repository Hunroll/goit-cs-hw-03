import psycopg2
import secret
from faker import Faker
import random

insert_users = """INSERT INTO users(email, fullname) VALUES(%s, %s)"""
insert_tasks = """INSERT INTO tasks(title, description, status_id, user_id) VALUES(%s, %s, %s, %s)"""

get_all_users = """select id from users"""
get_all_statuses = """select id from status"""
        

def fill_database():
    f = Faker()
    try:
        with psycopg2.connect(database=secret.dbName, user=secret.dbUser, password=secret.dbPassword, host=secret.dbHost, port=secret.dbPort) as conn:
            cursor = conn.cursor()

            # Створення юзерів
            users = list([(f.email(),f.name()) for _ in range(100)])
            cursor.executemany(insert_users, users)
            conn.commit()

            # Збір id юзерів
            cursor.execute(get_all_users)
            res = cursor.fetchall()
            user_ids = list([item[0] for item in res])
            
            # Збір id статусів
            cursor.execute(get_all_statuses)
            res = cursor.fetchall()
            statuses = list([item[0] for item in res])

            # Створення тасок для рандомних юзерів з рандомним статусом
            num_of_users = len(user_ids)
            num_of_statuses = len(statuses)
            tasks = []
            for _ in range(1000):
                user_id = user_ids[random.randint(0, num_of_users - 1)]
                status_id = statuses[random.randint(0, num_of_statuses - 1)]
                title = ' '.join(f.words(4))
                desc = ' '.join(f.words(random.randint(10, 40)))
                tasks.append((title, desc, status_id, user_id))
            cursor.executemany(insert_tasks, tasks)
            conn.commit()
    except Exception as e:
        print('Error filling DB!')
        print(e)


fill_database()