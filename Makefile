.PHONY: test clean help

# === 변수 정의 ===
TEST_SCOPE         ?= unit
TEST_TARGETS       ?= tests/unit
ENABLE_COVERAGE    ?= false

ifeq ($(ENABLE_COVERAGE), true)
	COV_OPT := --cov=src/
else
	COV_OPT :=
endif

export TEST_TARGETS
export COV_OPT

# === 테스트 실행 ===
test:
	docker compose -f docker/test/compose.$(TEST_SCOPE).yml up --build -d $(TEST_SCOPE)-test; \
	docker wait $(TEST_SCOPE)-test; \
	docker logs $(TEST_SCOPE)-test; \
	docker compose -f docker/test/compose.$(TEST_SCOPE).yml down