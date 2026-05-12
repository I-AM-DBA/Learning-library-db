CREATE DATABASE library;

\c library;

-- create author table
CREATE TABLE authors (
    author_id          serial          PRIMARY KEY,
    author_name        varchar(255)    NOT NULL
);

-- create category table
CREATE TABLE categories (
    category_id         serial          PRIMARY KEY,
    category_name       varchar(255)    NOT NULL
);

-- create sub_category table
CREATE TABLE sub_categories (
    sub_category_id     serial          PRIMARY KEY,
    category_id         integer         NOT NULL,
    sub_category_name   varchar(255)    NOT NULL,
    CONSTRAINT fk_sub_categories_category FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
);

-- create publisher table
CREATE TABLE publishers (
    publisher_id        serial          PRIMARY KEY,
    publisher_name      varchar(255)    NOT NULL,
    publisher_phone     varchar(31)     NULL,
    manager_name        varchar(255)    NULL
);

-- create books table
CREATE TYPE books_status AS ENUM ('A', 'B');
CREATE TABLE books (
    book_id             serial          PRIMARY KEY,
    title               varchar(255)    NOT NULL DEFAULT '',
    publisher_id        integer         NULL,
    location_name       varchar(255)    NULL,
    sub_category_id     integer         NULL,
    isbn                varchar(17)     NULL,
    created_date        date            NOT NULL DEFAULT CURRENT_DATE,
    published_year      smallint        NULL,
    status              books_status    NOT NULL DEFAULT 'A',
    is_damaged          boolean         NOT NULL DEFAULT FALSE,
    original_title      varchar(255)    NULL,
    call_no             varchar(63)     NULL,
    CONSTRAINT fk_books_publisher FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE RESTRICT,
    CONSTRAINT fk_books_sub_category FOREIGN KEY (sub_category_id) REFERENCES sub_categories(sub_category_id) ON DELETE SET NULL
);

-- create book_author_refs table
CREATE TABLE book_author_refs (
    auth_book_id    serial      PRIMARY KEY,
    book_id         integer     NOT NULL,
    author_id       integer     NOT NULL,
    CONSTRAINT fk_book_author_refs_book FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_book_author_refs_author FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);

-- create users table
CREATE TYPE users_type AS ENUM ('정회원', '준회원');
CREATE TYPE users_status AS ENUM ('active', 'inactive', 'banned', 'sleep');
CREATE TABLE users (
    user_id                 serial          PRIMARY KEY ,
    user_type               users_type      NOT NULL DEFAULT '준회원',
    user_status             users_status    NOT NULL DEFAULT 'active',
    loan_available_date     date            NULL DEFAULT CURRENT_DATE,
    loaned_book_count       smallint        NOT NULL DEFAULT 0
);

-- create users_info table
CREATE TABLE users_info (
    user_id     integer         PRIMARY KEY,
    name        varchar(255)    NOT NULL,
    birth_date  date            NULL,
    phone       varchar(31)     NULL,
    address     varchar(255)    NULL,
    CONSTRAINT fk_users_info_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- create users_secret table
CREATE TABLE users_secret (
    user_id         integer         PRIMARY KEY,
    email           varchar(255)    NOT NULL,
    password_hash   char(80)        NULL,
    CONSTRAINT fk_users_secret_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- create loans table
CREATE TABLE loans (
    loan_id             serial          PRIMARY KEY,
    user_id             integer         NOT NULL,
    book_id             integer         NOT NULL,
    loan_date           timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_extended         boolean         DEFAULT FALSE,
    return_date         timestamp       NULL,
    CONSTRAINT fk_loans_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_loans_book FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

-- create reservation table
CREATE TABLE reservation (
    reserved_id     serial          PRIMARY KEY,
    user_id         integer         NOT NULL,
    book_id         integer         NOT NULL,
    reserved_at     timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_res_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_res_book FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);
