# 2026 Fall Backend Study

멋쟁이사자처럼 백엔드 스터디를 위한 FastAPI 프로젝트입니다.

현재는 서버 상태를 확인하는 `GET /health` 엔드포인트만 제공합니다.

## 개발 환경

- Python 3.13
- FastAPI
- uv (패키지 및 가상환경 관리)
- pytest (테스트)
- Ruff (린트 및 포맷)

## 시작하기

### 1. uv 설치

macOS에서 Homebrew를 사용한다면 다음 명령으로 설치할 수 있습니다.

```bash
brew install uv
```

다른 설치 방법은 [uv 공식 설치 문서](https://docs.astral.sh/uv/getting-started/installation/)를 참고하세요.

### 2. 가상환경 및 의존성 준비

```bash
uv sync
```

이 명령은 프로젝트 루트에 `.venv`를 만들고 `uv.lock`에 고정된 의존성을 설치합니다.
별도로 Conda 환경을 활성화할 필요는 없습니다. `.venv`는 Git에 포함되지 않습니다.

### 3. 개발 서버 실행

```bash
uv run fastapi dev app/main.py
```

서버가 실행되면 다음 주소를 확인할 수 있습니다.

- Health check: <http://127.0.0.1:8000/health>
- Swagger UI: <http://127.0.0.1:8000/docs>

## 품질 검사

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

코드를 자동으로 포맷하려면 다음 명령을 실행합니다.

```bash
uv run ruff format .
```

## Conda를 계속 사용하고 싶다면

Conda 환경에서도 실행할 수 있지만, 팀원마다 환경이 달라지는 것을 막기 위해 이 저장소에서는
`uv`가 관리하는 `.venv` 사용을 권장합니다. Conda를 사용할 경우에도 패키지를 직접 `pip install`하지
말고 아래처럼 lock 파일을 기준으로 설치하세요.

```bash
conda create -n likelion-backend python=3.13
conda activate likelion-backend
uv sync --active
```

이 방식은 현재 활성화된 Conda 환경에 의존성을 동기화합니다. 한 프로젝트에서 Conda 환경과 `.venv`를
동시에 사용할 필요는 없습니다.
