from operator import ge
from uuid import UUID, uuid4
import pytest
from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from core.genre.application.use_cases.update_genre import UpdateGenre
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def action_genre(movie_category: Category) -> Genre:
    return Genre(name="Action", is_active=True, categories={movie_category.id})


@pytest.fixture
def sport_genre(movie_category: Category, documentary_category: Category) -> Genre:
    return Genre(
        name="Sport",
        is_active=True,
        categories={documentary_category.id, movie_category.id},
    )


@pytest.fixture
def sci_fi_genre() -> Genre:
    return Genre(
        name="Sci-fi",
        is_active=True,
    )


@pytest.fixture
def category_repository_with_categories(
    movie_category: Category, documentary_category: Category
) -> CategoryRepository:
    repository = InMemoryCategoryRepository()
    repository.save(category=movie_category)
    repository.save(category=documentary_category)
    return repository


@pytest.fixture
def genre_repository() -> GenreRepository:
    return InMemoryGenreRepository()


@pytest.fixture
def update_genre_use_case(
    genre_repository: GenreRepository,
    category_repository_with_categories: CategoryRepository,
) -> UpdateGenre:
    return UpdateGenre(
        genre_repository=genre_repository,
        category_repository=category_repository_with_categories,
    )


@pytest.fixture
def empty_category_repository() -> CategoryRepository:
    return InMemoryCategoryRepository()


class TestUpdateGenre:

    def test_update_genre_all_fields(
        self,
        genre_repository: GenreRepository,  # starts empty
        documentary_category: Category,
        update_genre_use_case: UpdateGenre,
        action_genre: Genre,  # action_genre atrributes : name="Action", is_active=True, categories={movie_category.id}
    ) -> None:

        genre_repository.save(genre=action_genre)

        new_action_genre: UpdateGenre.Input = (
            UpdateGenre.Input(  # all fields are different (except id)
                id=action_genre.id,
                name="Action and Adventure",
                is_active=False,
                categories={documentary_category.id},
            )
        )

        update_genre_use_case.execute(input=new_action_genre)

        updated_action_genre: Genre = genre_repository.get_by_id(id=action_genre.id)

        assert updated_action_genre.id == action_genre.id
        assert updated_action_genre.name == "Action and Adventure"
        assert updated_action_genre.is_active is False
        assert updated_action_genre.categories == {documentary_category.id}

    def test_update_genre_name_only(
        self,
        genre_repository: GenreRepository,  # starts empty
        action_genre: Genre,
        update_genre_use_case: UpdateGenre,
    ) -> None:

        genre_repository.save(genre=action_genre)

        new_action_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="Action and Adventure",
            is_active=True,
            categories=set(),
        )

        update_genre_use_case.execute(input=new_action_genre)

        updated_action_genre: Genre = genre_repository.get_by_id(id=action_genre.id)

        assert updated_action_genre.id == action_genre.id
        assert updated_action_genre.name == "Action and Adventure"
        assert updated_action_genre.is_active is True
        assert updated_action_genre.categories == action_genre.categories

    def test_update_genre_is_active_only(
        self,
        genre_repository: GenreRepository,  # starts empty
        action_genre: Genre,
        update_genre_use_case: UpdateGenre,
    ) -> None:

        genre_repository.save(genre=action_genre)

        new_action_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="Action",
            is_active=False,
            categories=set(),
        )

        update_genre_use_case.execute(input=new_action_genre)

        updated_action_genre: Genre = genre_repository.get_by_id(id=action_genre.id)

        assert updated_action_genre.id == action_genre.id
        assert updated_action_genre.name == "Action"
        assert updated_action_genre.is_active is False
        assert updated_action_genre.categories == action_genre.categories

    def test_update_genre_adding_category(
        self,
        genre_repository: GenreRepository,  # starts empty
        category_repository_with_categories: CategoryRepository,
        documentary_category: Category,
        movie_category: Category,
        action_genre: Genre,  # action_genre atrributes : name="Action", is_active=True, categories={movie_category.id}
    ) -> None:

        genre_repository.save(genre=action_genre)

        new_action_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="Action",
            is_active=True,
            categories={documentary_category.id, movie_category.id},
        )

        update_genre_use_case: UpdateGenre = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository_with_categories,
        )

        update_genre_use_case.execute(input=new_action_genre)

        updated_action_genre: Genre = genre_repository.get_by_id(id=action_genre.id)

        assert updated_action_genre.id == action_genre.id
        assert updated_action_genre.name == "Action"
        assert updated_action_genre.is_active is True
        assert updated_action_genre.categories == {
            documentary_category.id,
            movie_category.id,
        }

    def test_update_genre_removing_category(
        self,
        genre_repository: GenreRepository,  # starts empty
        category_repository_with_categories: CategoryRepository,
        documentary_category: Category,
        update_genre_use_case: UpdateGenre,
        sport_genre: Genre,  # sport_genre attributes : name="Sport", is_active=True, categories={documentary_category.id, movie_category.id}
    ) -> None:

        genre_repository.save(genre=sport_genre)

        new_sport_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=sport_genre.id,
            name="Sport",
            is_active=True,
            categories={documentary_category.id},
        )

        update_genre_use_case.execute(input=new_sport_genre)

        updated_sport_genre: Genre = genre_repository.get_by_id(id=sport_genre.id)

        assert updated_sport_genre.id == sport_genre.id
        assert updated_sport_genre.name == "Sport"
        assert updated_sport_genre.is_active is True
        assert updated_sport_genre.categories == {documentary_category.id}

    def test_update_genre_replace_category(
        self,
        genre_repository: GenreRepository,  # starts empty
        documentary_category: Category,
        update_genre_use_case: UpdateGenre,
        action_genre: Genre,  # action_genre atrributes : name="Action", is_active=True, categories={movie_category.id}
    ) -> None:

        genre_repository.save(genre=action_genre)

        new_action_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="Action",
            is_active=True,
            categories={documentary_category.id},
        )

        update_genre_use_case.execute(input=new_action_genre)

        updated_action_genre: Genre = genre_repository.get_by_id(id=action_genre.id)

        assert updated_action_genre.id == action_genre.id
        assert updated_action_genre.name == "Action"
        assert updated_action_genre.is_active is True
        assert updated_action_genre.categories == {documentary_category.id}

    def test_update_genre_not_found(
        self,
        genre_repository: GenreRepository,  # starts empty
        update_genre_use_case: UpdateGenre,
        action_genre: Genre,
    ) -> None:
        genre_repository.save(genre=action_genre)

        non_existent_genre_id: UUID = uuid4()

        new_action_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=non_existent_genre_id,
            name="Action and Adventure",
            is_active=False,
            categories=set(),
        )

        with pytest.raises(
            GenreNotFound,
            match="Not possible to update genre with id .* because it was not found",
        ) as exc_info:
            update_genre_use_case.execute(input=new_action_genre)

        assert str(non_existent_genre_id) in str(exc_info.value)

    def test_update_genre_with_invalid_related_categories(
        self,
        genre_repository: GenreRepository,
        action_genre: Genre,
        update_genre_use_case: UpdateGenre,
    ) -> None:

        genre_repository.save(genre=action_genre)

        non_registered_category_id: UUID = uuid4()

        new_action_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="Action and Adventure",
            is_active=False,
            categories={non_registered_category_id},
        )

        with pytest.raises(
            RelatedCategoriesNotFound,
            match="Categories with provided IDs not found: .*",
        ) as exc_info:
            update_genre_use_case.execute(input=new_action_genre)

        missing_category_ids_string = ", ".join(
            str(missing_category_id)
            for missing_category_id in new_action_genre.categories
        )

        assert missing_category_ids_string in str(exc_info.value)

    def test_update_genre_with_invalid_genre_name_empty(
        self,
        genre_repository: GenreRepository,  # starts empty
        action_genre: Genre,
        update_genre_use_case: UpdateGenre,
    ) -> None:

        genre_repository.save(genre=action_genre)

        new_action_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="",
            is_active=False,
            categories=set(),
        )

        with pytest.raises(InvalidGenre) as exc_info:
            update_genre_use_case.execute(input=new_action_genre)

        assert "name cannot be empty" == str(exc_info.value)

    def test_update_genre_with_invalid_long_name(
        self,
        genre_repository: GenreRepository,  # starts empty
        action_genre: Genre,
        update_genre_use_case: UpdateGenre,
    ) -> None:

        genre_repository.save(genre=action_genre)

        new_action_genre: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="a" * 256,  # invalid name
            is_active=False,
            categories=set(),
        )

        with pytest.raises(InvalidGenre) as exc_info:
            update_genre_use_case.execute(input=new_action_genre)

        assert "name cannot be longer than 255 characters" == str(exc_info.value)
