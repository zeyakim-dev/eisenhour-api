# Step 1: 베이스 이미지 설정 (python:3.12 이미지 사용)
FROM python:3.12-slim

# Step 2: 작업 디렉토리 설정
WORKDIR /app

# Step 3: 의존성 파일 복사
COPY pyproject.toml poetry.lock /app/

# Step 4: Poetry 설치
RUN pip install poetry

# Step 5: 의존성 설치
RUN poetry install --no-root --verbose --without dev

# Step 6: 애플리케이션 코드 복사
COPY src /app/src

# Step 7: 실행 명령어 설정
CMD ["python", "src/eisenhour-api/main.py"]
