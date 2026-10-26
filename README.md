# 2026 Fall Backend Study

7주차 CRUD 완성 코드입니다. 입력·출력 Model, HTTP 처리, SQL을 app/main.py에 모아 둡니다.
DB 연결 함수는 app/database.py에 둡니다. 8주차에는 Model · Repository · Router로 분리합니다.

| Endpoint | 동작 |
| --- | --- |
| GET / | Hello World |
| GET /health | 서버 상태. DB 연결 검사는 아님 |
| GET /users?limit=20 | id 순서로 조회. limit은 1~100 |
| GET /users/{user_id} | 단건 조회. 없으면 404, 정수가 아니면 422 |
| POST /users | 사용자 생성. 201, 중복 email은 409 |
| PATCH /users/{user_id} | name만 수정. 없으면 404 |
| DELETE /users/{user_id} | 삭제. 204, 없으면 404 |

목록 응답은 6주차 자료에 맞춘 `{"items": [...]}`입니다.
사용자 응답 필드는 id, name, email입니다. password_hash는 반환하지 않습니다.
회원가입·로그인·JWT·Supabase Auth는 아직 구현하지 않았습니다.
이후 주차의 기존 수업 자료는 그대로 남겨 둡니다.

## Supabase 연결

1. 학습용 project를 만들고 SQL Editor에서 app/sqls/schemas.sql을 실행합니다.
   기존 users 테이블이 있으면 삭제하지 말고 구조를 먼저 확인하세요.
2. app/sqls/seed_users.sql을 실행하면 가상 사용자 30명이 들어갑니다.
   재실행 시 기존 email은 건너뛰며 기존 데이터를 변경하지 않습니다.
3. Connect → Session pooler → View parameters에서 연결값을 확인합니다.
   Session pooler는 port 5432를 사용하고 IPv4 환경에서도 접속할 수 있습니다.
4. 프로젝트 루트에서 실행합니다.

```bash
cp .env.example .env.local
```

.env.local에 정확한 PGHOST, PGUSER, PGDATABASE, PGPASSWORD를 입력하세요.
PGPASSWORD는 DB 비밀번호이며 API key가 아닙니다.
이미 설정된 환경 변수는 .env.local보다 우선합니다.
SSL 암호화(sslmode=require) 및 5초 연결 제한을 사용합니다.
require는 서버 인증서까지 검증하지 않습니다. 배포 시 CA 인증서를 설정하고
verify-full을 사용하세요.

학습 SQL은 RLS를 켜고 anon/authenticated 접근을 차단합니다.
이 코드는 서버에서 DB role로 접속합니다. publishable key로 직접 조회하지 않습니다.
postgres 접속 정보는 학습용 서버에만 두고 frontend나 Git에 넣지 마세요.

## 실행

Python 3.13 및 uv를 사용합니다.

```bash
uv sync
uv run fastapi dev app/main.py
```

Swagger UI: http://127.0.0.1:8000/docs

```bash
curl 'http://127.0.0.1:8000/users?limit=2'
curl 'http://127.0.0.1:8000/users/1'
```

단건 조회 id는 실제 목록에서 확인하세요. id가 연속이라고 가정하지 않습니다.
SQL Editor에서 이름을 변경한 뒤 API를 다시 조회해 데이터 반영을 확인하세요.
DB 연결 오류는 404로 숨기지 않고 서버 오류로 유지합니다.

## Dummy data

!dummy-no-login은 실제 hash가 아닌 로그인 불가 placeholder입니다.
조회·CRUD 실습용입니다. 로그인 수업 전에 PasswordHash.recommended()로
생성한 실제 hash로 교체해야 합니다. public.users는 auth.users와 별개입니다.

## 검사

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

테스트는 DB 연결을 mock 처리합니다. 실제 연결은 .env.local 설정 후
GET /users로 확인하세요.

연결 가이드: https://supabase.com/docs/guides/database/connecting-to-postgres
