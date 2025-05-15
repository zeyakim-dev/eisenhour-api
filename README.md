# 🧭 eisenhour-api

eisenhour-api는 도메인 기반 설계를 바탕으로 구축된 Python 백엔드 API 프로젝트입니다. Entity, AggregateRoot, ValueObject 등의 핵심 개념을 구현하여 확장성과 유지보수성을 고려한 구조를 제공합니다.

---

## 🛠️ 기술 스택
    - 언어: Python 3.11
    - 패키지 관리: uv
    - 테스트 프레임워크: pytest
    - 정적 분석 도구: mypy, ruff
    - CI/CD: GitHub Actions
    - 컨테이너화: Docker, Docker Compose

---

## 🚀 시작하기

### 1. 레포지토리 클론 및 디렉토리 이동

```bash
git clone https://github.com/zeyakim-dev/eisenhour-api.git
cd eisenhour-api
```
### 2. 의존성 설치

uv를 사용하여 프로젝트의 의존성을 설치합니다:
```bash
uv sync
```

### 3. 가상 환경 생성 (선택 사항)

uv를 사용하여 가상 환경을 생성할 수 있습니다:
```bash
uv venv
```

### 4. 애플리케이션 실행

Docker Compose를 사용하여 애플리케이션을 실행합니다:
```bash
docker compose up
```

## 📁 프로젝트 구조

```bash
eisenhour-api/
├── src/
│   ├── main.py
│   ├── domain/
├── tests/
├── uv.lock
├── pyproject.toml
└── README.md
```

---

## 🖼️ 스크린샷

---

## 📌 주요 기능

* 기능 1: 설명
* 기능 2: 설명

---

## 🧪 테스트 실행

다음 명령어로 테스트를 실행할 수 있습니다:
```bash
uv run pytest
```

---

## 📄 라이선스


---

## 🙋‍♂️ 개발자 정보

* **이름**: 최지석
* **이메일**: zeyakimdev@gmail.com
* **GitHub**: [github.com/zeyakim-dev](https://github.com/zeyakim-dev)
