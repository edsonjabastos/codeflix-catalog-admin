from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSaveInMemoryCategoryRepository:
    
    def test_can_save_category(self) -> None:
        repository = InMemoryCategoryRepository()
        category = Category("Movie")

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category


class TestGetByIdInMemoryCategoryRepository:
        
        def test_can_get_category_by_id(self) -> None:
            repository = InMemoryCategoryRepository()
            category = Category("Movie")
            repository.save(category)
    
            category_found = repository.get_by_id(category.id)
    
            assert category_found == category