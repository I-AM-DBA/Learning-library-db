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


class SqlWriter:
    def __init__(self, path: Path, *, compress: bool = False):
        self.__compress: bool = compress

        suffix: str = ".sql.gz" if self.__compress else ".sql"
        self.__path: Path = path.with_suffix(suffix)

        self.__file: TextIOWrapper | None = None

    def __enter__(self):
        self.open()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        if self.__file is not None:
            raise RuntimeError("File is already open.")

        self.__path.parent.mkdir(mode=0o755, parents=True, exist_ok=True)

        if self.__compress:
            self.__file = gzip.open(self.__path, "wt", encoding="utf-8")
        else:
            self.__file = open(self.__path, "w", encoding="utf-8")

    def close(self):
        if self.__file is None:
            raise RuntimeError("File is not open.")

        self.__file.close()
        self.__path.chmod(0o644)

    def write(self, data: str):
        if self.__file is None:
            raise RuntimeError("File is not open.")

        self.__file.write(data)

    def write_line(self, line: str):
        self.write(line)
        self.write("\n")


class BaseSqlWriter(SqlWriter):
    _BASE_DIRECTORY = "./initdb.d"

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

        return data.strip().translate(BaseSqlWriter._ESCAPE_TABLE)

    def __init__(
        self,
        filename: str,
        schema: "BaseSqlWriter.Schema",
        *,
        compress: bool = False,
    ):
        super().__init__(Path(self._BASE_DIRECTORY) / filename, compress=compress)

        self._DATABASE_NAME = schema["database_name"]
        self._TABLE_NAME = schema["table_name"]
        self._ATTRIBUTES = schema["attributes"]

    def open(self):
        super().open()

        self.write_line(f"\\c {self._DATABASE_NAME}")
        self.write_line(
            f"COPY {self._TABLE_NAME} ({', '.join(self._ATTRIBUTES)}) FROM STDIN WITH (NULL ' ');"
        )

    def close(self):
        self.write_line("\\.")

        super().close()

    def write_row(self, *columns: str | None):
        escaped_columns = [self._escape_data(col) for col in columns]
        self.write_line("\t".join(escaped_columns))

    class Schema(TypedDict):
        database_name: str
        table_name: str
        attributes: list[str]


class AuthorsSql(BaseSqlWriter):
    def __init__(self, *, compress: bool = False):
        super().__init__(
            "20-authors",
            {
                "database_name": "library",
                "table_name": "authors",
                "attributes": ["author_name"],
            },
            compress=compress,
        )

        self._author_count = 0

    def write_author(self, name: str | None) -> str | None:
        """
        저자 이름을 입력받아 SQL 파일에 작성 및 저자 기본키 반환
        """
        if name is None:
            return None

        name = name.strip()
        if not name:
            return None

        self.write_row(name)
        self._author_count += 1

        return str(self._author_count)


class BooksSql(BaseSqlWriter):
    @staticmethod
    def refine_title(title: str) -> str:
        return re.sub(r"'{2,}", "'", title)

    @staticmethod
    def call_no_to_sub_category(call_no: str | None) -> str | None:
        if call_no is None:
            return None

        call_no = call_no.strip()
        if not call_no:
            return None

        try:
            n = int(call_no[:3])
            return str((n // 10) + 1)
        except ValueError:
            return None

    @staticmethod
    def refine_published_year(published_year: str | None) -> str | None:
        if published_year is None:
            return None

        published_year = published_year.strip()
        if not published_year or not published_year.isdigit():
            return None

        return published_year

    def __init__(self, *, compress: bool = False):
        super().__init__(
            "22-books",
            {
                "database_name": "library",
                "table_name": "books",
                "attributes": [
                    "title",
                    "publisher_id",
                    "location_name",
                    "sub_category_id",
                    "isbn",
                    "created_date",
                    "published_year",
                    "call_no",
                ],
            },
            compress=compress,
        )

        self._book_count = 0

    def write_book(
        self,
        title: str,
        publisher_id: str | None,
        location_name: str | None,
        isbn: str | None,
        created_date: str | None,
        published_year: str | None,
        call_no: str | None,
    ) -> str:
        """
        도서를 입력받아 SQL 파일에 작성 및 도서 기본키 반환
        """
        self.write_row(
            BooksSql.refine_title(title),
            publisher_id,
            location_name,
            BooksSql.call_no_to_sub_category(call_no),
            isbn,
            created_date,
            BooksSql.refine_published_year(published_year),
            call_no,
        )

        self._book_count += 1

        return str(self._book_count)


class BookAuthorRefsSql(BaseSqlWriter):
    def __init__(self, *, compress: bool = False):
        super().__init__(
            "23-book-author-refs",
            {
                "database_name": "library",
                "table_name": "book_author_refs",
                "attributes": ["book_id", "author_id"],
            },
            compress=compress,
        )

    def write_ref(self, book_id: str, author_id: str):
        """
        도서-저자 참조를 입력받아 SQL 파일에 작성
        """
        self.write_row(book_id, author_id)


class PublishersSql(BaseSqlWriter):
    def __init__(self, *, compress: bool = False):
        super().__init__(
            "21-publishers",
            {
                "database_name": "library",
                "table_name": "publishers",
                "attributes": ["publisher_name"],
            },
            compress=compress,
        )

        self.__publisher_map: dict[str, int] = {}

    def write_publisher(self, name: str | None) -> str | None:
        """
        출판사 이름을 입력받아 SQL 파일에 작성 및 출판사 기본키 반환
        """
        if name is None:
            return None

        name = name.strip()
        if not name:
            return None

        id = self.__publisher_map.get(name)
        if id is not None:
            return str(id)

        self.write_row(name)

        id = len(self.__publisher_map) + 1
        self.__publisher_map[name] = id

        return str(id)


class Main:
    @staticmethod
    def run():
        with (
            AuthorsSql(compress=True) as authors_sql,
            BookAuthorRefsSql(compress=True) as book_author_refs_sql,
            BooksSql(compress=True) as books_sql,
            PublishersSql(compress=True) as publishers_sql,
        ):
            print("Preparing data...")

            total_lines = 0
            for progress in LibraryArchive().readRecords():
                # filtering record with invalid title
                title = progress["record"].title
                if title is None:
                    continue

                title = title.strip()
                if not title or len(title) > 255:
                    continue

                # write author
                author_id = authors_sql.write_author(progress["record"].author)

                # write publisher
                publisher_id = publishers_sql.write_publisher(progress["record"].publer)

                # write book
                book_id = books_sql.write_book(
                    title,
                    publisher_id,
                    progress["record"].loca_name,
                    progress["record"].isbn,
                    progress["record"].create_date,
                    progress["record"].publer_year,
                    progress["record"].call_no,
                )

                # write book-author references
                if author_id is not None:
                    book_author_refs_sql.write_ref(book_id, author_id)

                # print progress
                current_line = progress["current_line"]
                if current_line % 1000 == 0:
                    total_lines = progress["total_lines"]
                    print(
                        f"Progress: {current_line} / {total_lines} ({(current_line / total_lines) * 100:.2f}%)",
                        end="\r",
                    )

            print(f"Progress: {total_lines} / {total_lines} (100.00%)")


if __name__ == "__main__":
    Main.run()
