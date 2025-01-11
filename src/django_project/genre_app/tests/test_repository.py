from uuid import uuid4
import pytest
from core.genre.domain.genre import Genre
from django_project.category_app.models import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.genre_app.models import Genre as GenreModel


@pytest.mark.django_db
class TestSave:

    def test_save_genre(self):
        action_genre: Genre = Genre(name="Action")
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()

        GenreModel.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreModel.objects.count() == 1
        action_genre_model: GenreModel = GenreModel.objects.first()
        assert action_genre_model.name == "Action"
        assert action_genre_model.is_active == True
        assert action_genre_model.id == action_genre.id

    def test_save_genre_with_one_related_category(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        category_repository: DjangoORMCategoryRepository = DjangoORMCategoryRepository()

        movie_category: Category = Category(
            name="Movie", description="Movies description"
        )
        category_repository.save(movie_category)
        action_genre: Genre = Genre(name="Action")
        action_genre.add_category(movie_category.id)

        assert GenreModel.objects.count() == 0
        genre_repository.save(action_genre)
        assert GenreModel.objects.count() == 1

        saved_action_genre: GenreModel = GenreModel.objects.first()
        assert saved_action_genre.name == "Action"
        assert saved_action_genre.is_active == True
        assert saved_action_genre.id == action_genre.id
        related_categorie: Category = saved_action_genre.categories.first()
        assert related_categorie.name == "Movie"
        assert related_categorie.description == "Movies description"
        assert related_categorie.id == movie_category.id

    def test_save_genre_with_two_related_categories(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        category_repository: DjangoORMCategoryRepository = DjangoORMCategoryRepository()

        movie_category: Category = Category(
            name="Movie", description="Movies description"
        )
        series_category: Category = Category(
            name="Series", description="Series description"
        )
        category_repository.save(movie_category)
        category_repository.save(series_category)

        action_genre: Genre = Genre(name="Action")
        action_genre.add_category(movie_category.id)
        action_genre.add_category(series_category.id)

        assert GenreModel.objects.count() == 0
        genre_repository.save(action_genre)
        assert GenreModel.objects.count() == 1

        saved_action_genre: GenreModel = GenreModel.objects.first()
        assert saved_action_genre.name == "Action"
        assert saved_action_genre.is_active == True
        assert saved_action_genre.id == action_genre.id

        related_categories = saved_action_genre.categories.all()
        assert related_categories.count() == 2

        movie_related_category: Category = related_categories.get(name="Movie")
        assert movie_related_category.name == "Movie"
        assert movie_related_category.description == "Movies description"
        assert movie_related_category.id == movie_category.id

        series_related_category: Category = related_categories.get(name="Series")
        assert series_related_category.name == "Series"
        assert series_related_category.description == "Series description"
        assert series_related_category.id == series_category.id


@pytest.mark.django_db
class TestGetById:

    def test_get_genre_by_id(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        action_genre: Genre = Genre(name="Action")

        assert GenreModel.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreModel.objects.count() == 1
        saved_action_genre: GenreModel = GenreModel.objects.first()

        assert genre_repository.get_by_id(saved_action_genre.id) == action_genre
        assert (
            genre_repository.get_by_id(saved_action_genre.id).id
            == saved_action_genre.id
        )
        assert genre_repository.get_by_id(saved_action_genre.id).name == "Action"

    def test_get_genre_by_id_with_one_related_category(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        category_repository: DjangoORMCategoryRepository = DjangoORMCategoryRepository()

        movie_category: Category = Category(
            name="Movie", description="Movies description"
        )
        category_repository.save(movie_category)

        action_genre: Genre = Genre(name="Action")
        action_genre.add_category(movie_category.id)
        assert GenreModel.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreModel.objects.count() == 1
        saved_action_genre: GenreModel = GenreModel.objects.first()

        assert genre_repository.get_by_id(saved_action_genre.id) == action_genre
        assert (
            genre_repository.get_by_id(saved_action_genre.id).id
            == saved_action_genre.id
        )
        assert genre_repository.get_by_id(saved_action_genre.id).name == "Action"

        related_category: Category = saved_action_genre.categories.first()
        assert related_category.name == "Movie"
        assert related_category.description == "Movies description"
        assert related_category.id == movie_category.id

    def test_get_genre_by_id_with_two_related_categories(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        category_repository: DjangoORMCategoryRepository = DjangoORMCategoryRepository()

        movie_category: Category = Category(
            name="Movie", description="Movies description"
        )
        series_category: Category = Category(
            name="Series", description="Series description"
        )
        category_repository.save(movie_category)
        category_repository.save(series_category)

        action_genre: Genre = Genre(name="Action")
        action_genre.add_category(movie_category.id)
        action_genre.add_category(series_category.id)
        assert GenreModel.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreModel.objects.count() == 1
        saved_action_genre: GenreModel = GenreModel.objects.first()

        assert genre_repository.get_by_id(saved_action_genre.id) == action_genre
        assert (
            genre_repository.get_by_id(saved_action_genre.id).id
            == saved_action_genre.id
        )
        assert genre_repository.get_by_id(saved_action_genre.id).name == "Action"
        assert genre_repository.get_by_id(saved_action_genre.id).categories == {
            movie_category.id,
            series_category.id,
        }

    def test_get_genre_by_id_not_found(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        non_existent_id = uuid4()
        assert genre_repository.get_by_id(str(non_existent_id)) == None


