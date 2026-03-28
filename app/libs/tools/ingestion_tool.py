from app.models.nodes import AnyNode, NamedNode
from app.repositories.main_interface_repository import (
    MainInterfaceRepository,
    NodeLabel,
    RelType,
)


class IngestionTool:
    def __init__(self, repository: MainInterfaceRepository) -> None:
        self.repository = repository

    async def ingest_node(self, node: AnyNode) -> None:
        identity_key = "name" if isinstance(node, NamedNode) else "id"
        await self.repository.merge_node(
            node.label, identity_key, node.model_dump(mode="json")
        )

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
        await self.repository.merge_relationship(
            NodeLabel(from_label),
            from_key,
            from_val,
            RelType(rel_type),
            NodeLabel(to_label),
            to_key,
            to_val,
        )
