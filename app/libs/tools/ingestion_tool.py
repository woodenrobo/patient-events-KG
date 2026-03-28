from app.repositories.main_interface_repository import MainInterfaceRepository


class IngestionTool:
    def __init__(self, repository: MainInterfaceRepository) -> None:
        self.repository = repository

    async def ingest_node(self, label: str, properties: dict) -> None:
        # stamp properties with id (uuid4), created_at, updated_at (datetime.now UTC)
        # cast label str -> NodeLabel enum
        # determine identity_key (e.g. "name" for most, "id" fallback)
        # await repository.merge_node(node_label, identity_key, properties)
        raise NotImplementedError

    async def ingest_relationship(
        self,
        from_label: str,
        from_key: str,
        from_val: str,
        rel_type: str,
        to_label: str,
        to_key: str,
        to_val: str,
    ) -> None:
        # cast label/rel_type strs -> NodeLabel / RelType enums
        # await repository.merge_relationship(...)
        raise NotImplementedError
