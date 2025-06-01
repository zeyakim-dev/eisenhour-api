class RepositoryNotFoundError(Exception):
    """Repository not found error"""

    def __init__(self, repository_name: str):
        self.repository_name = repository_name
        super().__init__(f"Repository {repository_name} not found")
