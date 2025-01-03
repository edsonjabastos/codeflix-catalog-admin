import pytest
from uuid import UUID, uuid4
from core.genre.domain.genre import Genre
from unittest.mock import patch


class TestGenre:

    def test_name_is_required(self) -> None:
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Genre()

    def test_name_must_have_less_than_255_characters(self) -> None:
        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
            Genre("a" * 256)

    def test_cannot_create_genre_with_empty_name(self) -> None:
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre("")

    def test_created_category_with_default_values(self) -> None:
        genre: Genre = Genre("Action")

        assert genre.name == "Action"
        assert genre.is_active is True
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_genre_is_created_with_provided_values(self) -> None:
        genre_id: UUID = uuid4()
        categories: set[UUID] = {uuid4(), uuid4()}
        genre: Genre = Genre(
            id=genre_id,
            name="Sci-Fi",
            is_active=False,
            categories=categories,
        )

        assert genre.id == genre_id
        assert genre.name == "Sci-Fi"
        assert genre.is_active is False
        assert genre.categories == categories

    def test_genre_str(self) -> None:
        genre_name: str = "Thriller"
        genre_is_active: bool = False
        genre_categories: set[UUID] = {uuid4(), uuid4()}
        genre = Genre(
            name=genre_name, is_active=genre_is_active, categories=genre_categories
        )

        assert (
            str(genre)
            == f"{genre_name} - ({genre_is_active}) - {len(genre_categories)} categories"
        )

    def test_genre_repr(self) -> None:
        genre_id: UUID = uuid4()
        genre_name: str = "Drama"
        genre: Genre = Genre(id=genre_id, name=genre_name)

        assert repr(genre) == f"<Genre {genre_name} ({genre_id})>"


class TestUpdateGenreName:

    def test_update_genre_name(self) -> None:
        genre: Genre = Genre("Action")

        genre.update_name("Adventure")

        assert genre.name == "Adventure"

    def test_update_genre_name_with_invalid_name(self) -> None:
        genre: Genre = Genre("Action")

        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
            genre.update_name("a" * 256)

    def test_cannot_update_genre_with_empty_name(self) -> None:
        genre: Genre = Genre("Action")

        with pytest.raises(ValueError, match="name cannot be empty"):
            genre.update_name("")

    def test_validate_name_called_on_update(self) -> None:
        genre: Genre = Genre("Action")

        with patch.object(genre, "validate_name") as mock_validate_name:
            genre.update_name("Adventure")
            mock_validate_name.assert_called_once()


class TestAddCategory:

    def test_add_category(self) -> None:
        genre: Genre = Genre("Action")
        category_id: UUID = uuid4()

        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories

    def test_can_add_multiple_categories(self) -> None:
        genre: Genre = Genre("Action")
        category_id_1: UUID = uuid4()
        category_id_2: UUID = uuid4()

        genre.add_category(category_id_1)
        genre.add_category(category_id_2)

        assert category_id_1 in genre.categories
        assert category_id_2 in genre.categories

    def test_validate_name_called_on_add_category(self) -> None:
        genre: Genre = Genre("Action")
        category_id: UUID = uuid4()

        with patch.object(genre, "validate_name") as mock_validate_name:
            genre.add_category(category_id)
            mock_validate_name.assert_not_called()


class TestRemoveCategory:

    def test_remove_category(self) -> None:
        genre: Genre = Genre("Action")
        category_id: UUID = uuid4()
        genre.add_category(category_id)

        assert category_id in genre.categories
        genre.remove_category(category_id)
        assert category_id not in genre.categories

    def test_validate_name_called_on_remove_category(self) -> None:
        genre: Genre = Genre("Action")
        category_id: UUID = uuid4()
        genre.add_category(category_id)

        with patch.object(genre, "validate_name") as mock_validate_name:
            genre.remove_category(category_id)
            mock_validate_name.assert_called_once()


class TestActivateGenre:

    def test_activate_inactive_genre(self) -> None:
        genre: Genre = Genre("Sci-Fi", is_active=False)

        genre.activate()

        assert genre.is_active is True

    def test_activate_active_genre(self) -> None:
        genre: Genre = Genre("Sci-Fi", is_active=True)

        genre.activate()

        assert genre.is_active is True

    def test_validate_name_called_on_activate(self) -> None:
        genre: Genre = Genre("Sci-Fi", is_active=False)

        with patch.object(genre, "validate_name") as mock_validate_name:
            genre.activate()
            mock_validate_name.assert_called_once()


class TestDeactivateGenre:
    def test_deactivate_inactive_genre(self) -> None:
        genre: Genre = Genre("Sci-Fi", is_active=False)

        genre.deactivate()

        assert genre.is_active is False

    def test_deactivate_active_genre(self) -> None:
        genre: Genre = Genre("Sci-Fi", is_active=True)

        genre.deactivate()

        assert genre.is_active is False

    def test_validate_name_called_on_deactivate(self) -> None:
        genre: Genre = Genre("Sci-Fi", is_active=True)

        with patch.object(genre, "validate_name") as mock_validate_name:
            genre.deactivate()
            mock_validate_name.assert_called_once()


class TestEquality:
    def test_when_genres_have_same_id_and_class(self) -> None:
        genre_id: UUID = uuid4()
        genre1: Genre = Genre(id=genre_id, name="Sci-Fi")
        genre2: Genre = Genre(id=genre_id, name="Sci-Fi")

        assert genre1 == genre2

    def test_equality_with_different_class(self) -> None:
        class FakeGenre: ...

        common_id: UUID = uuid4()
        genre: Genre = Genre(id=common_id, name="Sci-Fi")
        fake_genre = FakeGenre()
        fake_genre.id = common_id

        assert genre != fake_genre
