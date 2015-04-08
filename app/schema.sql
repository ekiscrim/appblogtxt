drop table if exists post;
create table post (
  id integer primary key autoincrement,
  title text not null,
  author text not null,
  textillo text not null
);