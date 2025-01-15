from uuid import uuid4
import pytest
from core.genre.domain.genre import Genre
from django_project.category_app.models import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.genre_app.models import Genre as GenreORM


@pytest.mark.django_db
class TestSave:

    def test_save_genre(self):
        action_genre: Genre = Genre(name="Action")
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()

        GenreORM.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreORM.objects.count() == 1
        action_genre_model: GenreORM = GenreORM.objects.first()
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

        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)
        assert GenreORM.objects.count() == 1

        saved_action_genre: GenreORM = GenreORM.objects.first()
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

        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)
        assert GenreORM.objects.count() == 1

        saved_action_genre: GenreORM = GenreORM.objects.first()
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

        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreORM.objects.count() == 1
        saved_action_genre: GenreORM = GenreORM.objects.first()

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
        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreORM.objects.count() == 1
        saved_action_genre: GenreORM = GenreORM.objects.first()

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
        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreORM.objects.count() == 1
        saved_action_genre: GenreORM = GenreORM.objects.first()

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
        assert genre_repository.get_by_id(str(non_existent_id)) is None


@pytest.mark.django_db
class TestDelete:

    def test_delete_genre(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        action_genre: Genre = Genre(name="Action")

        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)
        assert GenreORM.objects.count() == 1

        saved_action_genre: GenreORM = GenreORM.objects.first()
        genre_repository.delete(saved_action_genre.id)
        assert GenreORM.objects.count() == 0

    def test_delete_genre_with_one_related_category(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        category_repository: DjangoORMCategoryRepository = DjangoORMCategoryRepository()

        movie_category: Category = Category(
            name="Movie", description="Movies description"
        )
        category_repository.save(movie_category)

        action_genre: Genre = Genre(name="Action")
        action_genre.add_category(movie_category.id)
        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreORM.objects.count() == 1
        saved_action_genre: GenreORM = GenreORM.objects.first()

        genre_repository.delete(saved_action_genre.id)
        assert GenreORM.objects.count() == 0

    def test_delete_genre_with_two_related_categories(self):
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
        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreORM.objects.count() == 1
        saved_action_genre: GenreORM = GenreORM.objects.first()

        genre_repository.delete(saved_action_genre.id)
        assert GenreORM.objects.count() == 0


@pytest.mark.django_db
class TestList:

    def test_list_genres(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        action_genre: Genre = Genre(name="Action")
        comedy_genre: Genre = Genre(name="Comedy")
        drama_genre: Genre = Genre(name="Drama")

        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)
        genre_repository.save(comedy_genre)
        genre_repository.save(drama_genre)

        assert GenreORM.objects.count() == 3
        genres = genre_repository.list()
        assert len(genres) == 3
        assert action_genre in genres
        assert comedy_genre in genres
        assert drama_genre in genres

    def test_list_genres_with_one_related_category(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        category_repository: DjangoORMCategoryRepository = DjangoORMCategoryRepository()

        movie_category: Category = Category(
            name="Movie", description="Movies description"
        )
        category_repository.save(movie_category)

        action_genre: Genre = Genre(name="Action")
        action_genre.add_category(movie_category.id)
        comedy_genre: Genre = Genre(name="Comedy")
        comedy_genre.add_category(movie_category.id)
        drama_genre: Genre = Genre(name="Drama")
        drama_genre.add_category(movie_category.id)

        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)
        genre_repository.save(comedy_genre)
        genre_repository.save(drama_genre)

        assert GenreORM.objects.count() == 3
        genres = genre_repository.list()
        assert len(genres) == 3
        assert action_genre in genres
        assert comedy_genre in genres
        assert drama_genre in genres

        action_genre_model: GenreORM = GenreORM.objects.get(name="Action")
        comedy_genre_model: GenreORM = GenreORM.objects.get(name="Comedy")
        drama_genre_model: GenreORM = GenreORM.objects.get(name="Drama")

        related_category: Category = action_genre_model.categories.first()
        assert related_category.name == "Movie"
        assert related_category.description == "Movies description"
        assert related_category.id == movie_category.id

        related_category = comedy_genre_model.categories.first()
        assert related_category.name == "Movie"
        assert related_category.description == "Movies description"
        assert related_category.id == movie_category.id

        related_category = drama_genre_model.categories.first()
        assert related_category.name == "Movie"
        assert related_category.description == "Movies description"
        assert related_category.id == movie_category.id


@pytest.mark.django_db
class TestUpdate:

    def test_update_genre(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        action_genre: Genre = Genre(name="Action")

        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)
        assert GenreORM.objects.count() == 1

        saved_action_genre: GenreORM = GenreORM.objects.first()
        updated_action_genre: Genre = Genre(
            id=saved_action_genre.id, name="Action Updated"
        )
        genre_repository.update(updated_action_genre)

        updated_action_genre_model: GenreORM = GenreORM.objects.get(
            id=saved_action_genre.id
        )
        assert updated_action_genre_model.name == "Action Updated"

    def test_update_genre_with_one_related_category(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        category_repository: DjangoORMCategoryRepository = DjangoORMCategoryRepository()

        movie_category: Category = Category(
            name="Movie", description="Movies description"
        )
        category_repository.save(movie_category)

        action_genre: Genre = Genre(name="Action")
        action_genre.add_category(movie_category.id)
        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreORM.objects.count() == 1
        saved_action_genre: GenreORM = GenreORM.objects.first()

        updated_action_genre: Genre = Genre(
            id=saved_action_genre.id, name="Action Updated"
        )
        updated_action_genre.add_category(movie_category.id)
        genre_repository.update(updated_action_genre)

        updated_action_genre_model: GenreORM = GenreORM.objects.get(
            id=saved_action_genre.id
        )
        assert updated_action_genre_model.name == "Action Updated"

        related_category: Category = updated_action_genre_model.categories.first()
        assert related_category.name == "Movie"
        assert related_category.description == "Movies description"
        assert related_category.id == movie_category.id

    def test_update_genre_with_two_related_categories(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        category_repository: DjangoORMCategoryRepository = DjangoORMCategoryRepository()

        movie_category: Category = Category(
            name="Movie", description="Movies description"
        )
        series_category: Category = Category(
            name="Series", description="Series description"
        )
        document_category: Category = Category(
            name="Documentary", description="Documentary description"
        )
        category_repository.save(movie_category)
        category_repository.save(series_category)
        category_repository.save(document_category)

        action_genre: Genre = Genre(name="Action")
        action_genre.add_category(movie_category.id)
        action_genre.add_category(series_category.id)
        assert GenreORM.objects.count() == 0
        genre_repository.save(action_genre)

        assert GenreORM.objects.count() == 1

        saved_action_genre: GenreORM = GenreORM.objects.first()
        updated_action_genre: Genre = Genre(
            id=saved_action_genre.id, name="Action Updated"
        )

        updated_action_genre.add_category(document_category.id)
        genre_repository.update(updated_action_genre)

        updated_action_genre_model: GenreORM = GenreORM.objects.get(
            id=saved_action_genre.id
        )

        assert updated_action_genre_model.name == "Action Updated"
        assert updated_action_genre_model.is_active == True
        related_categories = updated_action_genre_model.categories.all()
        assert related_categories.count() == 1

        movie_related_category: Category = related_categories.get(name="Documentary")
        assert movie_related_category.name == "Documentary"
        assert movie_related_category.description == "Documentary description"
        assert movie_related_category.id == document_category.id

    def test_update_genre_not_found(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        non_existent_id = uuid4()
        updated_action_genre: Genre = Genre(id=non_existent_id, name="Action Updated")
        assert genre_repository.update(updated_action_genre) is None

    def test_update_genre_with_one_related_category_not_found(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        non_existent_id = uuid4()
        updated_action_genre: Genre = Genre(id=non_existent_id, name="Action Updated")
        updated_action_genre.add_category(non_existent_id)
        assert genre_repository.update(updated_action_genre) is None

    def test_update_genre_with_invalid_empty_name(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        action_genre: Genre = Genre(name="Action")
        genre_repository.save(action_genre)

        saved_action_genre: GenreORM = GenreORM.objects.first()
        with pytest.raises(ValueError, match="name cannot be empty"):
            updated_action_genre: Genre = Genre(id=saved_action_genre.id, name="")
            genre_repository.update(updated_action_genre)

        assert GenreORM.objects.first().name == "Action"

    def test_update_genre_with_invalid_large_name(self):
        genre_repository: DjangoORMGenreRepository = DjangoORMGenreRepository()
        action_genre: Genre = Genre(name="Action")
        genre_repository.save(action_genre)

        saved_action_genre: GenreORM = GenreORM.objects.first()
        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
            updated_action_genre: Genre = Genre(
                id=saved_action_genre.id, name="a" * 256
            )
            genre_repository.update(updated_action_genre)

        assert GenreORM.objects.first().name == "Action"
