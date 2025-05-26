from uuid import UUID


class EntityNotFoundError(Exception):
    """엔터티 조회 실패에 대한 예외입니다.

    저장소에서 주어진 ID를 가진 엔터티를 찾지 못했을 때 발생합니다.
    """

    def __init__(self, repository_name: str, id: UUID):
        """예외 메시지를 설정하여 초기화합니다.

        Args:
            repository_name (str): 엔터티를 조회한 저장소의 이름.
            id (str): 조회 대상 엔터티의 식별자.
        """
        self.message = f"{id} not found in {repository_name}"
        super().__init__(self.message)
