.. _ubiquitous_language:

유비쿼터스 언어 (Ubiquitous Language)
====================================

:도메인: Eisenhower 매트릭스를 활용한 개인 일정관리 시스템
:이해관계자: 개인 사용자
:지속적 개선: 필요 시 업데이트
:문서 형식: reStructuredText

이 문서는 Eisenhower 매트릭스를 이용한 일정관리 도메인에서 팀원과 이해관계자 간 원활한 의사소통을 위해 핵심 용어를 정의하고, 각 용어의 업무 의미를 일관되게 이해할 수 있도록 구성되었습니다.

---

1. 개요 및 정의
--------------

Eisenhower 매트릭스는 작업의 **긴급도(Urgency)**와 **중요도(Importance)**를 기준으로 네 가지 분류(제1~제4분면)로 나누어 우선순위를 결정하는 프레임워크입니다. 이를 통해 사용자는 즉시 처리할 작업과 장기 전략을 구분하여 효율적으로 관리할 수 있습니다.

---

2. 용어집 (Glossary)
-------------------

| 용어               | 정의                                                         | 매트릭스 분류         |
|--------------------|--------------------------------------------------------------|-----------------------|
| Task               | 사용자가 수행하는 개별 업무 단위                              | —                     |
| Urgency            | 즉시 대응해야 하는 정도 (예: 마감 임박)                       | 축(감도)              |
| Importance         | 조직적·개인적 목표 달성에 기여하는 정도                        | 축(중요성)            |
| Quadrant I         | 긴급하면서 중요한 업무 (즉시 실행)                            | Urgent & Important    |
| Quadrant II        | 중요하지만 긴급하지 않은 업무 (계획 후 실행)                   | Important & Not Urgent|
| Quadrant III       | 긴급하지만 중요하지 않은 업무 (위임 가능)                      | Urgent & Not Important|
| Quadrant IV        | 긴급하지 않고 중요하지 않은 업무 (제외 또는 연기)              | Not Urgent & Not Important|

---

3. 용어 도출 방법
-----------------

- **AI 협업 워크숍**: ChatGPT와의 브레인스토밍을 통해 초기 용어를 발굴
- **자기 검토**: 개인 경험 기반으로 정의 검증 및 보완
- **업데이트 절차**: 주요 개념이 추가되거나 변경될 때마다 해당 섹션을 수정하고 이력 기록

---

4. 적용 지침
-----------

- **코드 네이밍**: 클래스와 함수 이름에 용어 반영 (예: `class QuadrantIIPlanner`)
- **문서 통일**: 전체 문서에서 동일한 용어 사용
- **버전 관리**: Git 커밋 메시지에 변경 사유 기재, 주기적 리뷰는 선택

---

5. 유지·관리
------------

- 새로운 용어나 업무 흐름 변경 시 즉시 반영
- 변경 내역은 `changelog.rst`에 요약하여 기록