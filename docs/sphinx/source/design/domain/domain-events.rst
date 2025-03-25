이벤트 문서
====================

1. 유저 관련 이벤트
----------------------
- **UserRegistered**: 사용자가 회원가입을 완료했을 때 발생하는 이벤트.
- **UserAuthenticationAttempted**: 사용자가 로그인 시도를 했을 때 발생하는 이벤트.
- **UserAuthenticated**: 사용자가 인증에 성공했을 때 발생하는 이벤트.
- **UserAuthenticationFailed**: 사용자가 인증에 실패했을 때 발생하는 이벤트.

2. 프로젝트 관련 이벤트
----------------------
- **ProjectCreated**: 프로젝트가 생성됨.
- **ProjectInvitationSended**: 프로젝트 초대가 전송됨.
- **ProjectInvitationAccepted**: 프로젝트 초대가 수락됨.
- **ProjectInvitationRejected**: 프로젝트 초대가 거절됨.
- **EpicCreated**: 새로운 에픽이 생성됨.
- **ProjectUpdated**: 프로젝트 정보(이름, 설명 등)가 변경됨.
- **ProjectDeleted**: 프로젝트가 삭제됨.
- **ProjectMemberAdded**: 프로젝트에 새로운 멤버가 추가됨.
- **ProjectMemberRemoved**: 프로젝트에서 멤버가 제거됨.
- **ProjectArchived**: 프로젝트가 보관(아카이브)됨.

3. 태스크 관련 이벤트
----------------------
- **TaskCreated**: 태스크가 생성됨.
- **TaskUpdated**: 태스크 정보가 변경됨.
- **TaskCompleted**: 태스크가 완료됨.
- **TaskDeleted**: 태스크가 삭제됨.
- **TaskAssigned**: 특정 사용자에게 태스크가 할당됨.
- **TaskDueDateUpdated**: 태스크의 마감일이 변경됨.
- **TaskPriorityChanged**: 태스크의 우선순위가 변경됨.
- **TaskUrgencyUpdated**: 태스크의 긴급도가 변경됨.
- **TaskDelegated**: 태스크가 다른 사용자에게 위임됨.

4. 커뮤니케이션 이벤트
----------------------
- **CommentCreated**: 댓글이 생성됨.
- **CommentUpdated**: 댓글이 수정됨.
- **CommentDeleted**: 댓글이 삭제됨.
- **ChatMessageSent**: 채팅 메시지가 전송됨.

