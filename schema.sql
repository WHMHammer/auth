create database auth character set utf8mb4;

create table auth.users(
    id int auto_increment primary key,
    -- user info
    username varchar(64) unique,
    email varchar(64) unique,
    avatar varchar(512),
    -- user status
    catagory varchar(32),
    status varchar(32) default 'unverified',
    -- security
    salt char(16),
    password_hash char(128),
    last_login_time int(10) default 0,
    session char(16),
    challenge char(16)
);