\c library

-- create books table
CREATE TYPE books_status AS ENUM ('A', 'B');
CREATE TABLE books (
    book_id             serial          PRIMARY KEY,
    title               varchar(255)    NOT NULL DEFAULT '',
    publisher           varchar(255)    NULL,
    location_name       varchar(255)    NULL,
    category            varchar(255)    NULL,
    category_list       varchar(255)    NULL,
    isbn                varchar(17)     NULL,
    author              varchar(255)    NULL,
    created_date        date            NOT NULL DEFAULT CURRENT_DATE,
    published_year      smallint        NULL,
    status              books_status    NOT NULL DEFAULT 'A',
    is_damaged          boolean         NOT NULL DEFAULT FALSE,
    original_title      varchar(255)    NULL,
    call_no             varchar(63)     NULL
);

-- insert data into books table
INSERT INTO books (
    title,
    publisher,
    location_name,
    isbn,
    author,
    created_date,
    published_year,
    call_no
)
SELECT
    REGEXP_REPLACE(title, '''{2,}', '''', 'g'),
    publer,
    loca_name,
    isbn,
    author,
    create_date::date,
    publer_year::smallint,
    call_no
FROM raw_books
WHERE length(title) <= 255 AND
    publer_year ~ '^[0-9]{4}$';

-- create users table
CREATE TYPE users_type AS ENUM ('정회원', '준회원');
CREATE TABLE users (
    user_id                 serial          PRIMARY KEY ,
    email                   varchar(255)    NOT NULL,
    password_hash           char(80)        NULL,
    name                    varchar(100)    NOT NULL,
    age                     date            NULL,
    phone                   integer         NULL,
    address                 varchar(255)    NULL,
    user_type               users_type      NOT NULL DEFAULT '준회원',
    loan_available_date     date            NULL DEFAULT CURRENT_DATE,
    loaned_book_count       smallint        NOT NULL DEFAULT 0
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
