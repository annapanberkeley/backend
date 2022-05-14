CREATE DATABASE tasksdb;
use tasksdb;

CREATE TABLE IF NOT EXISTS tasks(
    `id` varchar(500) PRIMARY KEY,
    `taskName` varchar(500) NOT NULL,
    `taskStatus` boolean NOT NULL,
    `notify` varchar(500) NOT NULL
);

INSERT INTO tasks VALUES
    ('task1', 'sweep floor', False, 'anna_pan@berkeley.edu'),
    ('task2', 'water plants', False, 'anna_pan@berkeley.edu');