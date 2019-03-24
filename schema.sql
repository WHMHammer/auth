create database auth character set utf8mb4;

use auth;

create table users(
    id int auto_increment primary key,
    username varchar(64) unique,
    salt char(16),
    password_hash char(128),
    email varchar(64) unique,
    catagory varchar(32),
    status varchar(32) default 'unverified',
    last_login_time int(10) default 0,
    challenge char(16)
);
