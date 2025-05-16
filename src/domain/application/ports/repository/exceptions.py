class EntityNotFoundError(Exception):
    def __init__(self, repository_name: str, id: str):
        self.message = f"{id} not found in {repository_name}"
        super().__init__(self.message)
