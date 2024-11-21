create table users(
	id SERIAL primary key,
	fullname VARCHAR(100),
	email VARCHAR(100) unique not null
);

create table status(
	id SERIAL primary key,
	name VARCHAR(50) unique not null
);

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
)

insert into status(name) values('New');
insert into status(name) values('In progress');
insert into status(name) values('Completed');
