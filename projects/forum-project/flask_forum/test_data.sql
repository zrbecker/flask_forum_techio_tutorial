insert into users ('username', 'password') values ('admin', 'password123')
insert into users ('username', 'password') values ('john', 'smith123')

insert into threads ('title') values ('my first thread')
insert into threads ('title') values ('another thread')

insert into posts ('user_id', 'thread_id', 'message')
  values (
    (select 'user_id' from users where 'username' = 'admin'),
    (select 'thread_id' from threads where 'title' = 'my first thread'),
    'First post!'
  )

insert into posts ('user_id', 'thread_id', 'message')
  values (
    (select 'user_id' from users where 'username' = 'john'),
    (select 'thread_id' from threads where 'title' = 'my first thread'),
    'second post!'
  )

insert into posts ('user_id', 'thread_id', 'message')
  values (
    (select 'user_id' from users where 'username' = 'john'),
    (select 'thread_id' from threads where 'title' = 'another thread'),
    'this is some words!'
  )
