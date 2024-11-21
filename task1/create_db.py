import psycopg2
import secret

# Цей скрипт є альтернативним до create_db.sql

def main():
    try:
        with psycopg2.connect(database=secret.dbName, user=secret.dbUser, password=secret.dbPassword, host=secret.dbHost, port=secret.dbPort) as conn:
            cursor = conn.cursor()

            # Створення таблиці юзерів
            cursor.execute("""
                           create table users(
                                id SERIAL primary key,
                                fullname VARCHAR(100),
                                email VARCHAR(100) unique not null
                            )""")
            
            # Створення таблиці статусів
            cursor.execute("""
                           create table status(
                                id SERIAL primary key,
                                name VARCHAR(50) unique not null
                            )""")
            cursor.executemany("""insert into status(name) values(%s)""", [('New',), ('In progress',), ('Completed',)])

            # Створення таблиці тасок
            cursor.execute("""
                           create table tasks(
                                id SERIAL primary key,
                                title VARCHAR(100) not null,
                                description text,
                                status_id INT not null,
                                user_id INT not null,
                                FOREIGN KEY (status_id) REFERENCES status (id)
                                    ON DELETE SET NULL
                                    ON UPDATE cascade,
                                FOREIGN KEY (user_id) REFERENCES users (id)
                                    ON DELETE cascade
                                    ON UPDATE cascade
                            )""")
            conn.commit()
    except Exception as e:
        print('Error creating DB!')
        print(e)

main()