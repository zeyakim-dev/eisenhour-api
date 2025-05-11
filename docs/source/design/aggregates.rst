.. _aggregates:

애그리게잇 (Aggregates)
=====================

:도메인: Eisenhower 매트릭스를 활용한 개인 일정관리 시스템
:이해관계자: 개인 사용자
:지속적 개선: 필요 시 업데이트
:문서 형식: reStructuredText

이 문서는 도메인 모델에서 트랜잭션 경계를 정의하는 핵심 개념인 애그리게잇(Aggregate)에 대해 설명합니다.
각 Aggregate의 Root 엔티티, 관련 밸류 오브젝트, 불변식(Invariants), 주요 유스케이스를 정리합니다.

---

1. 설계 지침
-----------

- **Aggregate**는 일관성 경계를 제공하며, 변경 시 모든 불변식이 만족되어야 합니다.
- 외부에는 **Aggregate Root**만 노출되고, 내부 엔티티나 밸류 오브젝트는 내부에서 참조합니다.
- **Command Bus** 패턴 하에서는 각 Aggregate Root에 대한 Command Handler가 도메인 로직을 실행합니다.

---

2. Aggregate 목록
----------------

이 프로젝트에서 정의한 Aggregate는 다음과 같습니다:

- **User Aggregate**
- **Project Aggregate**
- **Task Aggregate**

---

3. User Aggregate
----------------

**Root 엔티티**: `User`

**밸류 오브젝트**:

- `Email` (중복 불가, 포맷 유효성 검증)
- `Credentials` (해시된 비밀번호 등)

**불변식(Invariants)**:

1. 이메일은 애플리케이션 전체에서 유일해야 한다.
2. 비밀번호 해시는 안전한 알고리즘을 사용해야 한다.

**주요 유스케이스 & Command Handler**:

- `RegisterUser` (이메일 중복 검사 → User 생성)
- `AuthenticateUser` (Credentials 검증)
- `UpdateProfile` (프로필 정보 수정)

---

4. Project Aggregate
--------------------

**Root 엔티티**: `Project`

**밸류 오브젝트**:

- `ProjectName` (비어 있을 수 없음)
- `Description` (선택 사항)

**불변식(Invariants)**:

1. 프로젝트 이름은 반드시 존재해야 한다.
2. 동일 사용자의 프로젝트 이름은 중복될 수 없다.

**주요 유스케이스 & Command Handler**:

- `CreateProject` (User 소유 관계 설정)
- `UpdateProject` (이름·설명 변경)
- `ArchiveProject` (프로젝트 비활성화)

---

5. Task Aggregate
-----------------

**Root 엔티티**: `Task`

**밸류 오브젝트**:

- `Title` (비어 있을 수 없음)
- `Description` (선택 사항)
- `DueDate` (선택 사항)
- `Quadrant` (Urgency/Importance 조합으로 분기)

**불변식(Invariants)**:

1. Task는 반드시 하나의 Quadrant에 속해야 한다.
2. 동일 Project 내에서 Task 제목은 중복될 수 없다.

**연관관계**:

- `Project` (ID 참조)
- `User` (할당자 ID 참조, 선택 사항)

**주요 유스케이스 & Command Handler**:

- `CreateTask` (Project 존재 여부 확인 → Task 생성)
- `UpdateTask` (제목·내용·DueDate·Quadrant 변경)
- `ChangeTaskStatus` (상태 변경)
- `DeleteTask` (삭제)

---

6. Task Aggregate 분리 결정
---------------------------

본 프로젝트에서는 다음 이유로 Task를 독립적인 Aggregate로 분리하여 설계합니다:

- **비즈니스 로직 복잡성**: Task는 자동 재분류, 상태 변환, 우선순위 조정 등 복합 로직을 수행합니다.
- **일관성 경계**: Task 변경 시 Project와 별도의 트랜잭션 경계가 필요해 성능 및 확장성에 유리합니다.
- **생명 주기 독립성**: Task는 Project와 관계없이 생성, 보관, 삭제가 가능합니다.
- **CQRS 적용**: Task 단위의 읽기·쓰기 모델 분리를 고려하기에 독립 Aggregate 구성이 적합합니다.

---