insert into users (username, password) values ('admin', 'password123');
insert into users (username, password) values ('john', 'smith123');

insert into threads (title) values ('My First Thread');
insert into threads (title) values ('Another Thread');

insert into posts (user_id, thread_id, message)
  values (
    (select user_id from users where username = 'admin'),
    (select thread_id from threads where title = 'My First Thread'),
    'First post!'
  );

insert into posts (user_id, thread_id, message)
  values (
    (select user_id from users where username = 'john'),
    (select thread_id from threads where title = 'My First Thread'),
    'second post!'
  );

insert into posts (user_id, thread_id, message)
  values (
    (select user_id from users where username = 'john'),
    (select thread_id from threads where title = 'Another Thread'),
    'this is some words!'
  );
