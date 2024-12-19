from abc import ABC, abstractmethod
from core.category.domain.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int) -> Category | None:
        raise NotImplementedError
