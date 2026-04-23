# Library DBMS

## Docker Compose 컨테이너 실행

1. `initdb.d` 디렉토리에 `o+rx` 권한을 지정합니다.
1. `initdb.d` 디렉토리 안의 파일들에 `o+r` 권한을 지정합니다.
1. `create-initdb-sql.py` Python 스크립트를 사용하여 공공데이터 삽입 SQL 파일을 생성합니다.
1. `.env.example` 파일을 `.env` 이름으로 복사 후 수정하여 데이터베이스의 접속 패스워드를 지정합니다.
1. `docker compose up` 명령을 이용하여 컨테이너를 실행합니다.
1. <http://localhost:8080> 에 접속하거나 SQL Client를 이용하여 DBMS에 접근합니다.

## DBMS 서버 정보

- Database: `library`
- Port: `5432/tcp`
- User: `postgres`
- Password: ( `.env` 파일에 명시한 비밀번호를 따름)

## initdb.d

데이터베이스 스키마 생성 및 데이터 삽입 / 초기화 스크립트가 위치한 디렉토리입니다.

- `0?-*.sql` : 스키마 생성 파일
- `1?-*.sql` : 공공데이터 삽입 파일
- `2?-*.sql` : 테스트용 더미 데이터 생성 및 삽입 파일

## Database 초기화

`pgdata` 라는 Named Volume으로 Database를 보존하도록 되어있으므로 해당 볼륨을 삭제하면 데이터가 초기화됩니다.
