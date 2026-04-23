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

    def write(self, line: str):
        self._file.write(line + "\n")

    def write_row(self, *columns: str):
        escaped_columns = [self._escape_data(col) for col in columns]
        self.write("\t".join(escaped_columns))


class Main:
    _BOOKS_SQL_FILENAME = "10-books.sql.gz"

    @staticmethod
    def run():
        with SqlGzWriter(Main._BOOKS_SQL_FILENAME) as books:
            books.write("\\c library")

            books.write(
                "COPY books (title, publisher, location_name, isbn, author, created_date, published_year, call_no) FROM STDIN WITH (NULL ' ');"
            )

            print("Preparing data...")
            total_lines = 0
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

                books.write_row(
                    title,
                    progress["record"].publer,
                    progress["record"].loca_name,
                    progress["record"].isbn,
                    progress["record"].author,
                    progress["record"].create_date,
                    published_year,
                    progress["record"].call_no,
                )

                current_line = progress["current_line"]
                if current_line % 1000 == 0:
                    total_lines = progress["total_lines"]
                    print(
                        f"Progress: {current_line} / {total_lines} ({(current_line / total_lines) * 100:.2f}%)",
                        end="\r",
                    )

            print(f"Progress: {total_lines} / {total_lines} (100.00%)")

            books.write("\\.")


if __name__ == "__main__":
    Main.run()
