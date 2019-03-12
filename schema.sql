drop database auth if exits;
create database auth character set utf8mb4;
use auth;

create table users(
    id int primary key,
    username varchar(32) unique,
    salt char(32),
    password_hash char(128),
    email varchar(64) unique,
    catagory varchar(32),
    status varchar(32) default 'unverified',
    last_login_time int(10) default 0,
    challenge char(32)
);