create database auth character set utf8mb4;

create table auth.users(
    id int not null auto_increment,
    -- user info
    username varchar(64) unique,
    email varchar(64) unique,
    avatar varchar(512),
    -- user status
    status varchar(32) default 'unverified',
    role varchar(32),
    -- password
    salt char(16),
    password_hash char(128),
    challenge char(16),
    primary key(id)
);

create table auth.sessions(
    user_id int not null,
    session char(16) not null,
    expire_time int(10) not null,
    foreign key(user_id) references auth.users(id)
);
