-- Отримати всі завдання певного користувача (юзер 42)
select 
	tasks.title, tasks.description, s.name as status
from tasks 
join status s on s.id = tasks.status_id 
where tasks.user_id = 42;


--Вибрати завдання за певним статусом
select 
	tasks.id, tasks.title, tasks.description, u.email as user, s."name" as status
from tasks 
join users u on u.id = tasks.user_id 
join status s on s.id = tasks.status_id 
where s."name" = 'New';


--Оновити статус конкретного завдання
update tasks t set status_id = (select id from status where "name" = 'In progress') where t.id = 51;
--перевірка
select t.id, s."name" from tasks t join status s on s.id = t.status_id  where t.id = 51;


--Отримати список користувачів, які не мають жодного завдання
select * from users where id not in (
	select user_id from tasks
)


--Додати нове завдання для конкретного користувача (Юзер 42)
insert into tasks(title, description, status_id, user_id) values ('Додати нове завдання', 'Додати нове завдання для конкретного користувача', 3, 42);


--Отримати всі завдання, які ще не завершено
select 
	tasks.id, tasks.title, tasks.description, u.email as user, s."name" as status
from tasks 
join users u on u.id = tasks.user_id 
join status s on s.id = tasks.status_id 
where s."name" <> 'Completed';


--Видалити конкретне завдання (1007)
delete from tasks where id = 1007;


--Знайти користувачів з певною електронною поштою
select * from users where lower(users.email) like 'matt%';


--Оновити ім'я користувача (14, знайдений в попередньому завданні)
update users set fullname = 'Matthew Obviously' where id = 14;


--Отримати кількість завдань для кожного статусу
select count(1) as "count", s."name" as status 
from tasks t 
join status s on t.status_id = s.id 
group by s.id;


--Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
select 
	tasks.id, u.email
from tasks 
join users u on u.id = tasks.user_id 
where u.email like '%@example.com';


--Отримати список завдань, що не мають опису
select * from tasks where description is null;


--Вибрати користувачів та їхні завдання, які є у статусі
select 
	u.id as user_id, u.fullname, u.email, tasks.id as task_id, tasks.title, tasks.description, s."name" as status
from tasks 
inner join users u on u.id = tasks.user_id 
inner join status s on s.id = tasks.status_id 
where s."name" = 'In progress';


--Отримати користувачів та кількість їхніх завдань
select 
	u.id, u.fullname, u.email, count(t.id)
from users u
left join tasks t on t.user_id = u.id 
group by u.id;



