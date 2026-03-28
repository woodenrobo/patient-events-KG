from app.repositories.main_interface_repository import MainInterfaceRepository


class QueryTool:
    def __init__(self, repository: MainInterfaceRepository) -> None:
        self.repository = repository

    async def modal_care_path(self, condition: str) -> list[dict]:
        return await self.repository.get_modal_care_path(condition)

    async def symptoms_preceding_diagnosis(self, condition: str) -> list[dict]:
        return await self.repository.get_symptoms_preceding_diagnosis(condition)

    async def medications_cooccurring_with_symptom(self, symptom: str) -> list[dict]:
        return await self.repository.get_medications_cooccurring_with_symptom(symptom)
