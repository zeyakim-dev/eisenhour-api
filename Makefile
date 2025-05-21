.PHONY: test clean help

# === 변수 정의 ===
TEST_SCOPE        	?= unit
TEST_TARGETS      	?= tests/unit
ENABLE_COVERAGE   	?= false
ENABLE_CLEANUP    	?= true

ifeq ($(ENABLE_COVERAGE),true)
	COV_OPT := --cov=src/
else
	COV_OPT :=
endif

ifeq ($(ENABLE_COVERAGE), true)
	CPY_COV_CMD := docker cp $(TEST_SCOPE)-test:/app/.coverage ./coverage.$(TEST_SCOPE)
else
	CPY_COV_CMD :=
endif

ifeq ($(ENABLE_CLEANUP),true)
	CLEANUP_CMD := docker compose -f docker/test/compose.$(TEST_SCOPE).yml down
else
	CLEANUP_CMD :=
endif

# === 테스트 실행 ===
test:
	TEST_TARGETS=$(TEST_TARGETS) \
	COV_OPT=$(COV_OPT) \
	docker compose -f docker/test/compose.$(TEST_SCOPE).yml up --build \
		--abort-on-container-exit \
		--exit-code-from $(TEST_SCOPE)-test \
		$(TEST_SCOPE)-test || echo "❌ Test failed: $(TEST_SCOPE)"
	$(CPY_COV_CMD)
	$(CLEANUP_CMD)
# === 수동 클린업 ===
clean:
	$(CLEANUP_CMD)