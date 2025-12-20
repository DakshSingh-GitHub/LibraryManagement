
CREATE DATABASE IF NOT EXISTS library;

USE library;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE books (
    book_id int primary key not null auto_increment,
    book_name varchar(255) not null,
    book_author varchar(255) not null,
    book_genre varchar(255) not null,
    book_publication_year int not null,
    book_issue_rate double default 130,
    book_quantity int not null default 1
);

CREATE TABLE visitors (
    visitor_uid int primary key not null auto_increment,
    visitor_fname varchar(255) not null,
    visitor_mname varchar(255),
    visitor_lname varchar(255),
    visitor_phone varchar(15) not null,
    visitor_email varchar(255),
    visitor_address varchar(255) not null,
    visitor_dateOfJoin date,
    books_issued int default 0,
    book_current_quantity INT
);


CREATE TABLE book_issues (
    issue_id int primary key not null auto_increment,
    book_id int not null,
    visitor_uid int not null,
    issue_date date not null,
    return_date date,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (visitor_uid) REFERENCES visitors(visitor_uid) ON UPDATE CASCADE ON DELETE CASCADE
);

# YYYY-MM-DD
insert into visitors(visitor_uid, visitor_fname, visitor_mname, visitor_lname, visitor_phone, visitor_email, visitor_address, visitor_dateOfJoin) values (1, 'Daksh', null, 'Singh', '9045390564', 'daksh.singh.2407@gmail.com', '256 Shiv Garden Bareilly', '2025-12-2');

insert into visitors(visitor_fname, visitor_mname, visitor_lname, visitor_phone, visitor_email, visitor_address, visitor_dateOfJoin) values ('Manas', null, 'Mangla', '8859020305', 'manasmanglaunstoppable1201@gmail.com', '45 Garden City Bareilly', '2025-12-6');


select * from visitors;
truncate table visitors;
DELETE FROM visitors where visitor_uid = 5;

UPDATE visitors SET visitor_address = '46 Garden City Bareilly' WHERE visitor_uid = 2;
DELETE FROM visitors WHERE visitor_uid = 6;

SELECT DATEDIFF('2024-05-20', '2024-05-10') AS 'DifferenceInDays';

INSERT INTO books(book_name, book_author, book_genre, book_publication_year, book_issue_rate, book_quantity)
VALUES
('ds', 'dsd', 'fe', 2025, 200, 4);

CREATE VIEW visitor_issue AS
    SELECT
        book_issues.issue_id AS 'issue_id',
        book_issues.issue_clear AS `issue_clear`,
        visitors.visitor_uid AS `visitor_uid`,
        CONCAT(visitors.visitor_fname, ' ', visitors.visitor_lname) AS `visitor_name`,
        books.book_id AS `book_id`,
        books.book_name AS 'book_name',
        books.book_author AS 'book_author'
    FROM visitors, book_issues, books
    WHERE
        book_issues.visitor_uid = visitors.visitor_uid and book_issues.book_id = books.book_id;

drop view visitor_issue;
