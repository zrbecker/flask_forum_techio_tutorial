drop table if exists users;
create table users(
  user_id integer primary key autoincrement,
  username text not null unique,
  password text not null
);

drop table if exists threads;
create table threads(
  thread_id integer primary key autoincrement,
  title text not null
);

drop table if exists posts;
create table posts(
  post_id integer primary key autoincrement,
  user_id integer not null,
  thread_id integer not null,
  message text not null,
  posted datetime default current_timestamp 
);
