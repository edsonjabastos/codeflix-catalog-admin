from uuid import uuid4
import pytest
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.value_objects import CastMemberType
from django_project.castmember_app.repository import DjangoORMCastMemberRepository
from django_project.castmember_app.models import CastMember as CastMemberORM


@pytest.mark.django_db
class TestSave:

    def test_save_castmember(self):
        jhon_castmember: CastMember = CastMember(name="Jhon", type=CastMemberType.ACTOR)
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )

        CastMemberORM.objects.count() == 0
        castmember_repository.save(jhon_castmember)

        assert CastMemberORM.objects.count() == 1
        jhon_castmember_model: CastMemberORM = CastMemberORM.objects.first()
        assert jhon_castmember_model.id == jhon_castmember.id
        assert jhon_castmember_model.name == "Jhon"
        assert jhon_castmember_model.type == jhon_castmember.type

    def test_save_castmember_two_castmembers(self):
        jhon_castmember: CastMember = CastMember(name="Jhon", type=CastMemberType.ACTOR)
        jane_castmember: CastMember = CastMember(
            name="Jane", type=CastMemberType.DIRECTOR
        )
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )

        CastMemberORM.objects.count() == 0
        castmember_repository.save(jhon_castmember)
        castmember_repository.save(jane_castmember)

        assert CastMemberORM.objects.count() == 2
        jhon_castmember_model: CastMemberORM = CastMemberORM.objects.get(
            name="Jhon"
        )
        assert jhon_castmember_model.id == jhon_castmember.id
        assert jhon_castmember_model.name == "Jhon"
        assert jhon_castmember_model.type == jhon_castmember.type

        jane_castmember_model: CastMemberORM = CastMemberORM.objects.get(
            name="Jane"
        )
        assert jane_castmember_model.id == jane_castmember.id
        assert jane_castmember_model.name == "Jane"
        assert jane_castmember_model.type == jane_castmember.type


@pytest.mark.django_db
class TestDelete:

    def test_delete_castmember(self):
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )
        action_castmember: CastMember = CastMember(
            name="Jhon", type=CastMemberType.ACTOR
        )

        assert CastMemberORM.objects.count() == 0
        castmember_repository.save(action_castmember)
        assert CastMemberORM.objects.count() == 1

        saved_action_castmember: CastMemberORM = CastMemberORM.objects.first()
        castmember_repository.delete(saved_action_castmember.id)
        assert CastMemberORM.objects.count() == 0

    def test_delete_castmember_not_found(self):
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )
        non_existent_id = uuid4()
        assert castmember_repository.delete(non_existent_id) is None


@pytest.mark.django_db
class TestList:

    def test_list_castmembers(self):
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )
        sylvie_castmember: CastMember = CastMember(
            name="Sylvester Stallone", type=CastMemberType.ACTOR
        )
        jim_castmember: CastMember = CastMember(
            name="Jim Carrey", type=CastMemberType.ACTOR
        )
        chris_castmember: CastMember = CastMember(
            name="Christopher Nolan", type=CastMemberType.DIRECTOR
        )

        assert CastMemberORM.objects.count() == 0
        castmember_repository.save(sylvie_castmember)
        castmember_repository.save(jim_castmember)
        castmember_repository.save(chris_castmember)

        assert CastMemberORM.objects.count() == 3
        castmembers = castmember_repository.list()
        assert len(castmembers) == 3
        assert sylvie_castmember in castmembers
        assert jim_castmember in castmembers
        assert chris_castmember in castmembers


@pytest.mark.django_db
class TestUpdate:

    def test_update_castmember(self):
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )
        sylvie_castmember: CastMember = CastMember(
            name="Sylvester Stallone", type=CastMemberType.ACTOR
        )
        castmember_repository.save(sylvie_castmember)

        assert CastMemberORM.objects.count() == 1
        saved_sylvie_castmember: CastMemberORM = CastMemberORM.objects.first()

        updated_sylvie_castmember: CastMember = CastMember(
            id=saved_sylvie_castmember.id,
            name="Sylvester Stallone Updated",
            type=CastMemberType.DIRECTOR,
        )
        castmember_repository.update(updated_sylvie_castmember)

    def test_update_castmember_not_found(self):
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )
        non_existent_id = uuid4()
        updated_action_castmember: CastMember = CastMember(
            id=non_existent_id, name="John Travolta", type=CastMemberType.ACTOR
        )
        assert castmember_repository.update(updated_action_castmember) is None

    def test_update_castmember_with_invalid_empty_name(self):
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )

        sylvie_castmember: CastMember = CastMember(
            name="Sylvester Stallone", type="ACTOR"
        )
        castmember_repository.save(sylvie_castmember)

        saved_action_castmember: CastMemberORM = CastMemberORM.objects.first()
        saved_action_castmember: CastMemberORM = CastMemberORM.objects.first()
        with pytest.raises(ValueError, match="name cannot be empty"):
            updated_action_castmember: CastMember = CastMember(
                id=saved_action_castmember.id,
                name="",
                type="ACTOR",
            )
            castmember_repository.update(updated_action_castmember)

        assert CastMemberORM.objects.first().name == "Sylvester Stallone"
        assert CastMemberORM.objects.first().type == "ACTOR"
        assert CastMemberORM.objects.first().id == saved_action_castmember.id

    def test_update_castmember_with_invalid_large_name(self):
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )
        sylvie_castmember: CastMember = CastMember(
            name="Sylvester Stallone", type="ACTOR"
        )
        castmember_repository.save(sylvie_castmember)

        saved_action_castmember: CastMemberORM = CastMemberORM.objects.first()

        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
            updated_action_castmember: CastMember = CastMember(
                id=saved_action_castmember.id, name="a" * 256, type="ACTOR"
            )
            castmember_repository.update(updated_action_castmember)

        assert CastMemberORM.objects.first().name == "Sylvester Stallone"
        assert CastMemberORM.objects.first().type == "ACTOR"

    def test_update_castmember_with_invalid_type(self):
        castmember_repository: DjangoORMCastMemberRepository = (
            DjangoORMCastMemberRepository()
        )
        action_castmember: CastMember = CastMember(
            name="Sylvester Stallone", type="ACTOR"
        )
        castmember_repository.save(action_castmember)

        saved_action_castmember: CastMemberORM = CastMemberORM.objects.first()
        with pytest.raises(ValueError, match="invalid type"):
            updated_action_castmember: CastMember = CastMember(
                id=saved_action_castmember.id, name="Sylvester Stallone", type="INVALID"
            )
            castmember_repository.update(updated_action_castmember)

        assert CastMemberORM.objects.first().name == "Sylvester Stallone"
        assert CastMemberORM.objects.first().type == "ACTOR"
