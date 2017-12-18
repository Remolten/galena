import pytest

from ..galena import galena


class Health(galena.Component):
    health = 1


class Velocity(galena.Component):
    required_components = (Health,)

    speed = 10
    direction = 180


@pytest.fixture
def game():
    yield galena.Game()


@pytest.fixture
def entity(game):
    yield game.create_entity()


class TestGalena:
    @staticmethod
    def test_reset(game, entity):
        game.add_component_to_entity(Health(), entity)

        game.reset()

        assert game.uid == 0
        assert len(game.entities) == 0
        assert len(game.components) == 0


class TestEntity:
    @staticmethod
    def test_create_entity(game, entity):
        assert entity == game.uid

    @staticmethod
    def test_remove_entity(game, entity):
        assert game.remove_entity(entity)
        assert entity not in game.entities

        with pytest.raises(KeyError):
            game.remove_entity(game.uid + 1)

    @staticmethod
    def test_entity_has(game, entity):
        assert not game.entity_has(entity, Health)
        assert not game.entity_has(entity, Health, Velocity)

        game.add_component_to_entity(Health(), entity)
        assert game.entity_has(entity, Health)

        with pytest.raises(TypeError):
            game.add_component_to_entity(Health(), entity)

        game.add_component_to_entity(Velocity(), entity)
        assert game.entity_has(entity, Health, Velocity)

    @staticmethod
    def test_entities_with(game, entity):
        game.add_component_to_entity(Health(), entity)
        game.add_component_to_entity(Velocity(), entity)

        assert entity in list(game.entities_with(Health))
        assert entity in list(game.entities_with(Velocity))


@pytest.mark.usefixtures('game', 'entity')
class TestComponents:
    @staticmethod
    def test_add_component_to_entity(game, entity):
        health_component = Health()
        velocity_component = Velocity()

        with pytest.raises(TypeError):
            game.add_component_to_entity(velocity_component, entity)
        assert not game.entity_has(entity, Velocity)
        assert velocity_component not in game.components[Velocity]

        game.add_component_to_entity(health_component, entity)
        assert game.entity_has(entity, Health)
        assert health_component == game.components[Health][entity]
        assert not health_component.required_by

        game.add_component_to_entity(velocity_component, entity)
        assert game.entity_has(entity, Velocity)
        assert velocity_component == game.components[Velocity][entity]
        assert Velocity in health_component.required_by

    @staticmethod
    def test_remove_component_from_entity(game, entity):
        health_component = Health()
        velocity_component = Velocity()

        game.add_component_to_entity(health_component, entity)
        game.add_component_to_entity(velocity_component, entity)

        with pytest.raises(TypeError):
            game.remove_component_from_entity(Health, entity)

        game.remove_component_from_entity(Velocity, entity)
        assert not game.entity_has(entity, Velocity)
        assert velocity_component not in game.components[Velocity]

        game.remove_component_from_entity(Health, entity)
        assert not game.entity_has(entity, Health)
        assert health_component not in game.components[Health]

    @staticmethod
    def test_get_components_of_type(game, entity):
        health_component = Health()
        velocity_component = Velocity()

        game.add_component_to_entity(health_component, entity)
        game.add_component_to_entity(velocity_component, entity)

        assert health_component in list(game.get_components_of_type(Health))
        assert velocity_component not in list(game.get_components_of_type(Health))  # noqa: E501

        assert velocity_component in list(game.get_components_of_type(Velocity))
        assert health_component not in list(game.get_components_of_type(Velocity))  # noqa: E501

    @staticmethod
    def test_get_components_for_entity(game, entity):
        health_component = Health()
        velocity_component = Velocity()

        game.add_component_to_entity(health_component, entity)
        game.add_component_to_entity(velocity_component, entity)

        assert health_component in list(game.get_components_for_entity(entity, Health))  # noqa: E501
        assert velocity_component in list(game.get_components_for_entity(entity, Velocity))  # noqa: E501

        multiple_components = list(game.get_components_for_entity(entity, Health, Velocity))  # noqa: E501
        assert health_component in multiple_components
        assert velocity_component in multiple_components
