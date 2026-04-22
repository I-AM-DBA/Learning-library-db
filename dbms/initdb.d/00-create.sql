CREATE DATABASE library;

\c library

CREATE TABLE raw_books (
    crityn              varchar(255),  -- 서평존재여부
    nbook_yn            varchar(255),  -- 신착도서여부
    lang_name           varchar(255),  -- 언어명
    lang                varchar(255),  -- 언어
    sub_loca_name       varchar(255),  -- 자료실 이름
    author              varchar(255),  -- 저자
    loca_name           varchar(255),  -- 소장처명
    title               varchar(1023), -- 자료명
    class_no            varchar(255),  -- 분류기호
    loan_status_name    varchar(255),  -- 대출상태메시지
    create_date         varchar(255),  -- 등록일
    page                varchar(255),  -- 페이지
    old_intrcn_yn       varchar(255),  -- 해제 여부
    isbn                varchar(255),  -- 국제표준도서번호
    onlnyn              varchar(255),  -- 온라인 유무
    publer              varchar(255),  -- 출판사
    bib_type_name       varchar(255),  -- 자료유형명
    oldyn               varchar(255),  -- 고서 유무
    urlyn               varchar(255),  -- URL링크 유무
    contry_name         varchar(255),  -- 국가코드명
    loca                varchar(255),  -- 소장처
    loan_status         varchar(255),  -- 대출상태코드
    sub_loca            varchar(255),  -- 자료실 코드
    absyn               varchar(255),  -- 초록 유무
    author_no           varchar(255),  -- 저자기호
    call_no             varchar(255),  -- 청구기호
    contry              varchar(255),  -- 국가코드
    publer_year         varchar(255),  -- 발행년
    struct_yn           varchar(255),  -- 목차 유무
    bib_type            varchar(255),  -- 자료유형코드
    ctrlno              varchar(255),  -- 자료코드
    vodyn               varchar(255),  -- VOD 유무
    append_info         varchar(255),  -- 딸림정보
    editon              varchar(255)   -- 판차
);

COMMENT ON COLUMN raw_books.crityn           IS '서평존재여부';
COMMENT ON COLUMN raw_books.nbook_yn         IS '신착도서여부';
COMMENT ON COLUMN raw_books.lang_name        IS '언어명';
COMMENT ON COLUMN raw_books.lang             IS '언어';
COMMENT ON COLUMN raw_books.sub_loca_name    IS '자료실 이름';
COMMENT ON COLUMN raw_books.author           IS '저자';
COMMENT ON COLUMN raw_books.loca_name        IS '소장처명';
COMMENT ON COLUMN raw_books.title            IS '자료명';
COMMENT ON COLUMN raw_books.class_no         IS '분류기호';
COMMENT ON COLUMN raw_books.loan_status_name IS '대출상태메시지';
COMMENT ON COLUMN raw_books.create_date      IS '등록일';
COMMENT ON COLUMN raw_books.page             IS '페이지';
COMMENT ON COLUMN raw_books.old_intrcn_yn    IS '해제 여부';
COMMENT ON COLUMN raw_books.isbn             IS '국제표준도서번호';
COMMENT ON COLUMN raw_books.onlnyn           IS '온라인 유무';
COMMENT ON COLUMN raw_books.publer           IS '출판사';
COMMENT ON COLUMN raw_books.bib_type_name    IS '자료유형명';
COMMENT ON COLUMN raw_books.oldyn            IS '고서 유무';
COMMENT ON COLUMN raw_books.urlyn            IS 'URL링크 유무';
COMMENT ON COLUMN raw_books.contry_name      IS '국가코드명';
COMMENT ON COLUMN raw_books.loca             IS '소장처';
COMMENT ON COLUMN raw_books.loan_status      IS '대출상태코드';
COMMENT ON COLUMN raw_books.sub_loca         IS '자료실 코드';
COMMENT ON COLUMN raw_books.absyn            IS '초록 유무';
COMMENT ON COLUMN raw_books.author_no        IS '저자기호';
COMMENT ON COLUMN raw_books.call_no          IS '청구기호';
COMMENT ON COLUMN raw_books.contry           IS '국가코드';
COMMENT ON COLUMN raw_books.publer_year      IS '발행년';
COMMENT ON COLUMN raw_books.struct_yn        IS '목차 유무';
COMMENT ON COLUMN raw_books.bib_type         IS '자료유형코드';
COMMENT ON COLUMN raw_books.ctrlno           IS '자료코드';
COMMENT ON COLUMN raw_books.vodyn            IS 'VOD 유무';
COMMENT ON COLUMN raw_books.append_info      IS '딸림정보';
COMMENT ON COLUMN raw_books.editon           IS '판차';
