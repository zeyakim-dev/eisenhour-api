from uuid import UUID


class ModelNotFoundError(Exception):
    """요청한 ID에 해당하는 모델을 찾을 수 없을 때 발생하는 예외입니다."""

    def __init__(self, model_name: str, id: UUID):
        """
        Args:
            model_name (str): 조회 실패한 모델 클래스 이름.
            id (UUID): 찾지 못한 엔터티의 식별자.
        """
        super().__init__(f"{model_name} with id {id} not found.")
