from uuid import UUID, uuid4

import pytest

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from core.genre.application.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
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
def category_repository_with_categories(
    movie_category, documentary_category
) -> CategoryRepository:
    return InMemoryCategoryRepository(categories=[movie_category, documentary_category])


@pytest.fixture
def genre_repository() -> GenreRepository:
    return InMemoryGenreRepository()


class TestListGenre:
    def test_list_genre_with_empty_repository(
        self, genre_repository: GenreRepository
    ) -> None:
        use_case: ListGenre = ListGenre(
            genre_repository=genre_repository,
        )

        output: ListGenre.Output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0

    def test_list_genre_with_populated_repository(
        self,
        movie_category: Category,
        documentary_category: Category,
        genre_repository: GenreRepository,
    ) -> None:
        romantic_genre = Genre(name="Romantic", categories={movie_category.id})
        sport_genre = Genre(
            name="Sport", categories={movie_category.id, documentary_category.id}
        )
        # estranho que salva gêneros no sem repositorio de categoria sem a certeza de que as categorias existem
        genre_repository.save(romantic_genre)
        genre_repository.save(sport_genre)

        use_case: ListGenre = ListGenre(
            genre_repository=genre_repository,
        )

        output: ListGenre.Output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 2
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=romantic_genre.id,
                    name=romantic_genre.name,
                    is_active=romantic_genre.is_active,
                    categories={movie_category.id},
                ),
                GenreOutput(
                    id=sport_genre.id,
                    name=sport_genre.name,
                    is_active=sport_genre.is_active,
                    categories={movie_category.id, documentary_category.id},
                ),
            ]
        )

    def test_list_genres_with_associated_categories(self):
        # category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        cat_1 = Category(name="Category 1", description="Category 1 description")
        # category_repository.save(cat_1)

        cat_2 = Category(name="Category 2", description="Category 2 description")
        # category_repository.save(cat_2)

        genre_drama = Genre(
            name="Drama",
            categories={cat_1.id, cat_2.id},
        )
        genre_repository.save(genre_drama)

        genre_romance = Genre(name="Romance")
        genre_repository.save(genre_romance)

        use_case = ListGenre(genre_repository=genre_repository)
        output = use_case.execute(ListGenre.Input())

        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre_drama.id,
                    name="Drama",
                    categories={cat_1.id, cat_2.id},
                    is_active=True,
                ),
                GenreOutput(
                    id=genre_romance.id,
                    name="Romance",
                    categories=set(),
                    is_active=True,
                ),
            ]
        )
