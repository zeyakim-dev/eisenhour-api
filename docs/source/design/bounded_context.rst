.. _bounded_contexts:

바운디드 컨텍스트 (Bounded Contexts)
===================================

:도메인: Eisenhower 매트릭스를 활용한 개인 일정관리 시스템
:이해관계자: 개인 사용자
:지속적 개선: 필요 시 업데이트
:문서 형식: reStructuredText

이 문서는 Eisenhower 매트릭스를 기반한 개인 일정관리 애플리케이션을 여러 의미적 경계(context)로 분할하여,
각 경계 안에서 일관된 도메인 모델과 용어를 사용하는 방법을 설명합니다.
또한, 전통적인 Service 레이어를 제거하고 Command Bus 패턴을 통해 엔드포인트가 직접 Command를 발행하고 처리 결과를 반환하는 구조를 제안합니다.

---

1. 개요
-------

바운디드 컨텍스트(Bounded Context)는 특정 도메인 모델과 유비쿼터스 언어(Ubiquitous Language)가 일관되게 적용되는
시스템 상의 논리적 경계입니다. 서로 다른 컨텍스트 간에는 모델과 용어가 달라질 수 있으며,
이를 명확한 경계로 구분함으로써 복잡도를 관리하고 모듈성을 강화합니다.

---

2. 주요 컨텍스트
----------------

애플리케이션을 다음과 같이 네 가지 주요 컨텍스트로 분리합니다. 각 컨텍스트는 Service 레이어 대신
Command Bus의 Command Handler를 통해 도메인 로직을 수행합니다:

- **User Context**
  - Command Handler: `RegisterUser`, `AuthenticateUser`, `UpdateProfile`
  - 데이터: User 엔티티, Credentials 밸류 오브젝트

- **Task Context**
  - Command Handler: `CreateTask`, `UpdateTask`, `DeleteTask`, `ChangeTaskStatus`
  - 데이터: Task 애그리게잇, TaskList 엔티티

- **Priority Context**
  - Command Handler: `CalculatePriority`, `ReassignQuadrant`
  - 데이터: Quadrant 밸류 오브젝트, PriorityScore 엔티티

- **Notification Context**
  - Command Handler: `ScheduleNotification`, `SendNotification`
  - 데이터: Notification 엔티티, DeliveryChannel 밸류 오브젝트

---

3. 컨텍스트 매핑 다이어그램
--------------------------

전통적인 Service 노드를 Command Handler로 대체한 Mermaid 다이어그램입니다:

```mermaid
flowchart LR
  subgraph UserContext[User Context]
    U[RegisterUserHandler]
    U2[AuthenticateUserHandler]
  end

  subgraph TaskContext[Task Context]
    T1[CreateTaskHandler]
    T2[UpdateTaskHandler]
  end

  subgraph PriorityContext[Priority Context]
    P1[CalculatePriorityHandler]
  end

  subgraph NotificationContext[Notification Context]
    N1[ScheduleNotificationHandler]
  end

  %% 엔드포인트 → 버스 → 핸들러 → 결과 반환
  Endpoint[Endpoint]
  Endpoint -- "CreateTask Command" --> Bus[Command Bus]
  Bus --> CreateTaskHandler
  CreateTaskHandler -->|응답| Endpoint

  %% 컨텍스트간 이벤트 흐름
  CreateTaskHandler -->|TaskCreated Event| CalculatePriorityHandler
  CalculatePriorityHandler -->|PriorityCalculated Event| ScheduleNotificationHandler
````

---

4. Command Bus 기반 통합 전략

---

* **엔드포인트 역할**: HTTP API 엔드포인트가 Command 객체를 생성하여 Command Bus에 적재(dispatch)합니다.
* **Command Bus**: 중앙 버스가 Command를 해당 컨텍스트의 Command Handler로 라우팅합니다.
* **Command Handler**: 각 컨텍스트 내부의 Handler가 도메인 엔티티를 조작하고, 처리 결과를 반환하거나 Domain Event를 발행합니다.
* **Domain Event**: Command 처리 후 생성된 이벤트는 필요한 다른 컨텍스트의 Command로 변환되어 재적재할 수 있습니다.
* **폐기된 Service 레이어**: Service 클래스 대신 Command Handler와 도메인 모델이 직접 협력하므로 구조가 간결해집니다.
* **비동기 처리가 필요한 경우**: 메시지 큐 시스템(Kafka, RabbitMQ 등)을 활용하여 Command 또는 Event를 비동기로 처리합니다.

---
