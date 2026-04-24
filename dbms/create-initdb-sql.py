#!/usr/bin/env python3

from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path
from typing import Generator, TypedDict
import gzip
import json
import re
import tarfile


class LibraryArchive:
    _ARCHIVE_FILENAME = "library-20260413.tar.gz"
    _JSON_FILENAME = "20260413.json"
    _SKIP_FIRST_LINES = 3

    def readRecords(self) -> Generator["_Progress", None, None]:
        with tarfile.open(self._ARCHIVE_FILENAME, "r:gz") as tar:
            json_file = tar.extractfile(self._JSON_FILENAME)
            if json_file is None:
                raise FileNotFoundError(
                    f"'{self._JSON_FILENAME}' not found in the archive."
                )

            # open the file as binary and count total lines
            total_line_count = 0
            for line in json_file:
                total_line_count += line.count(b"\n")
            json_file.seek(0)

            # open the file as text and read records
            with TextIOWrapper(json_file, encoding="utf-8") as file:
                line_count = self._SKIP_FIRST_LINES

                # skip first some lines (metadata)
                for _ in range(self._SKIP_FIRST_LINES):
                    next(file)

                # read and yield records
                for line in file:
                    line_count += 1

                    line = line.rstrip(",\n")

                    try:
                        json_line = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    yield {
                        "record": self._LibraryRecord(json_line),
                        "total_lines": total_line_count,
                        "current_line": line_count,
                    }

    @dataclass(frozen=True)
    class _LibraryRecord:
        _record: dict

        @property
        def crityn(self) -> str:
            """서평존재여부"""
            return self._record["crityn"]

        @property
        def nbook_yn(self) -> str:
            """신착도서여부"""
            return self._record["nbook_yn"]

        @property
        def lang_name(self) -> str:
            """언어명"""
            return self._record["lang_name"]

        @property
        def lang(self) -> str:
            """언어"""
            return self._record["lang"]

        @property
        def sub_loca_name(self) -> str:
            """자료실 이름"""
            return self._record["sub_loca_name"]

        @property
        def author(self) -> str:
            """저자"""
            return self._record["author"]

        @property
        def loca_name(self) -> str:
            """소장처명"""
            return self._record["loca_name"]

        @property
        def title(self) -> str:
            """자료명"""
            return self._record["title"]

        @property
        def class_no(self) -> str:
            """분류기호"""
            return self._record["class_no"]

        @property
        def loan_status_name(self) -> str:
            """대출상태메시지"""
            return self._record["loan_status_name"]

        @property
        def create_date(self) -> str:
            """등록일"""
            return self._record["create_date"]

        @property
        def page(self) -> str:
            """페이지"""
            return self._record["page"]

        @property
        def old_intrcn_yn(self) -> str:
            """해제 여부"""
            return self._record["old_intrcn_yn"]

        @property
        def isbn(self) -> str:
            """국제표준도서번호"""
            return self._record["isbn"]

        @property
        def onlnyn(self) -> str:
            """온라인 유무"""
            return self._record["onlnyn"]

        @property
        def publer(self) -> str:
            """출판사"""
            return self._record["publer"]

        @property
        def bib_type_name(self) -> str:
            """자료유형명"""
            return self._record["bib_type_name"]

        @property
        def oldyn(self) -> str:
            """고서 유무"""
            return self._record["oldyn"]

        @property
        def urlyn(self) -> str:
            """URL링크 유무"""
            return self._record["urlyn"]

        @property
        def contry_name(self) -> str:
            """국가코드명"""
            return self._record["contry_name"]

        @property
        def loca(self) -> str:
            """소장처"""
            return self._record["loca"]

        @property
        def loan_status(self) -> str:
            """대출상태코드"""
            return self._record["loan_status"]

        @property
        def sub_loca(self) -> str:
            """자료실 코드"""
            return self._record["sub_loca"]

        @property
        def absyn(self) -> str:
            """초록 유무"""
            return self._record["absyn"]

        @property
        def author_no(self) -> str:
            """저자기호"""
            return self._record["author_no"]

        @property
        def call_no(self) -> str:
            """청구기호"""
            return self._record["call_no"]

        @property
        def contry(self) -> str:
            """국가코드"""
            return self._record["contry"]

        @property
        def publer_year(self) -> str:
            """발행년"""
            return self._record["publer_year"]

        @property
        def struct_yn(self) -> str:
            """목차 유무"""
            return self._record["struct_yn"]

        @property
        def bib_type(self) -> str:
            """자료유형코드"""
            return self._record["bib_type"]

        @property
        def ctrlno(self) -> str:
            """자료코드"""
            return self._record["ctrlno"]

        @property
        def vodyn(self) -> str:
            """VOD 유무"""
            return self._record["vodyn"]

        @property
        def append_info(self) -> str:
            """딸림정보"""
            return self._record["append_info"]

        @property
        def editon(self) -> str:
            """판차"""
            return self._record["editon"]

    class _Progress(TypedDict):
        record: "LibraryArchive._LibraryRecord"
        total_lines: int
        current_line: int


class SqlGzWriter:
    _BASE_DIRECTORY = Path("./initdb.d")
    _ESCAPE_TABLE = str.maketrans(
        {
            "\\": "\\\\",
            "\n": "\\n",
            "\r": "\\r",
            "\t": "\\t",
        }
    )

    @staticmethod
    def _escape_data(data: str | None) -> str:
        if data is None:
            return " "

        return data.strip().translate(SqlGzWriter._ESCAPE_TABLE)

    def __init__(self, filename: str):
        self._path = self._BASE_DIRECTORY / filename

    def __enter__(self):
        self._path.parent.mkdir(exist_ok=True)
        self._file = gzip.open(self._path, "wt", encoding="utf-8")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()
        self._path.chmod(0o644)

    def write_line(self, line: str):
        self._file.write(line)
        self._file.write("\n")

    def write_row(self, *columns: str | None):
        escaped_columns = [self._escape_data(col) for col in columns]
        self.write_line("\t".join(escaped_columns))


class SqlPack:
    _AUTHORS_SQL_FILENAME = "10-authors.sql.gz"
    _BOOK_AUTHOR_REFS_SQL_FILENAME = "13-book-author-refs.sql.gz"
    _BOOKS_SQL_FILENAME = "12-books.sql.gz"
    _PUBLISHERS_SQL_FILENAME = "11-publishers.sql.gz"

    def __init__(self) -> None:
        self.authors = SqlGzWriter(SqlPack._AUTHORS_SQL_FILENAME)
        self.book_author_refs = SqlGzWriter(SqlPack._BOOK_AUTHOR_REFS_SQL_FILENAME)
        self.books = SqlGzWriter(SqlPack._BOOKS_SQL_FILENAME)
        self.publishers = SqlGzWriter(SqlPack._PUBLISHERS_SQL_FILENAME)

    def __enter__(self):
        self.authors.__enter__()
        self.book_author_refs.__enter__()
        self.books.__enter__()
        self.publishers.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.authors.__exit__(exc_type, exc_value, traceback)
        self.book_author_refs.__exit__(exc_type, exc_value, traceback)
        self.books.__exit__(exc_type, exc_value, traceback)
        self.publishers.__exit__(exc_type, exc_value, traceback)


class Main:
    @staticmethod
    def call_no_to_sub_category(call_no: str) -> str | None:
        if not call_no:
            return None

        try:
            n = int(call_no[:3])
            return str((n // 10) + 1)
        except ValueError:
            return None

    @staticmethod
    def run():
        with SqlPack() as pack:
            pack.authors.write_line("\\c library")
            pack.authors.write_line(
                "COPY authors (author_name) FROM STDIN WITH (NULL ' ');"
            )

            publishers_map: dict[str, str] = {}
            pack.publishers.write_line("\\c library")
            pack.publishers.write_line(
                "COPY publishers (publisher_name) FROM STDIN WITH (NULL ' ');"
            )

            pack.books.write_line("\\c library")
            pack.books.write_line(
                "COPY books (title, publisher_id, location_name, sub_category_id, isbn, created_date, published_year, call_no) FROM STDIN WITH (NULL ' ');"
            )

            pack.book_author_refs.write_line("\\c library")
            pack.book_author_refs.write_line(
                "COPY book_author_refs (book_id, author_id) FROM STDIN WITH (NULL ' ');"
            )

            print("Preparing data...")
            total_lines = 0
            book_count = 0
            author_count = 0
            for progress in LibraryArchive().readRecords():
                title = progress["record"].title
                if len(title) > 255:
                    continue

                published_year = progress["record"].publer_year
                if published_year is None:
                    continue

                published_year = published_year.strip()  # trim
                if not published_year or not published_year.isdigit():
                    continue

                # trim title and replace multiple single quotes with one
                title = title.strip()
                title = re.sub(r"'{2,}", "'", title)

                # process publishers
                publisher_id = None
                publisher_name = progress["record"].publer
                if publisher_name is not None and publisher_name.strip():
                    if publisher_name in publishers_map:
                        publisher_id = publishers_map[publisher_name]
                    else:
                        publisher_id = str(len(publishers_map) + 1)
                        publishers_map[publisher_name] = publisher_id
                        pack.publishers.write_row(publisher_name)

                # get sub category from call_no
                call_no = progress["record"].call_no
                sub_category = Main.call_no_to_sub_category(call_no)

                # write books
                pack.books.write_row(
                    title,
                    publisher_id,
                    progress["record"].loca_name,
                    sub_category,
                    progress["record"].isbn,
                    progress["record"].create_date,
                    published_year,
                    progress["record"].call_no,
                )
                book_count += 1

                # write authors and book-author references
                authors = progress["record"].author
                if authors is not None and authors.strip():
                    pack.authors.write_row(authors)
                    author_count += 1
                    pack.book_author_refs.write_row(str(book_count), str(author_count))

                # print progress
                current_line = progress["current_line"]
                if current_line % 1000 == 0:
                    total_lines = progress["total_lines"]
                    print(
                        f"Progress: {current_line} / {total_lines} ({(current_line / total_lines) * 100:.2f}%)",
                        end="\r",
                    )

            print(f"Progress: {total_lines} / {total_lines} (100.00%)")

            pack.authors.write_line("\\.")
            pack.book_author_refs.write_line("\\.")
            pack.books.write_line("\\.")
            pack.publishers.write_line("\\.")


if __name__ == "__main__":
    Main.run()
