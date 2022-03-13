insert into movie_types (movie_type) values ('Action');

insert into movies (title, description, movie_type, rating)
values ('Action 1', 'This is action 1 movie', 'Action',  8);

insert into movies (title, description, movie_type, rating)
values ('Adventure 1', 'This is adventure 1 movie', 'Adventure',  6);

insert into user_types (user_type) values ('Admin');
insert into user_types (user_type) values ('User');

insert into user (email, name, surname, user_type)
values ('admin@example.com', 'Admin', 'Admin', 'Admin');

insert into user (email, name, surname, user_type)
values ('user@example.com', 'User1', 'User1', 'User');

insert into movie_types (movie_type) values ('Horror');

insert into movies (title, description, movie_type, rating)
values ('The Shining', 'A family is forced to live in an isolated room in order to avoid the presence of the killer.', 'Horror', 9);