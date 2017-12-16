import pytest

from ..src import galena


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

        assert game._uid == 0
        assert len(game._entities) == 0
        assert len(game._components) == 0


class TestEntity:
    @staticmethod
    def test_create_entity(game, entity):
        assert entity == game._uid

    @staticmethod
    def test_remove_entity(game, entity):
        assert game.remove_entity(entity)
        assert entity not in game._entities
        assert not game.remove_entity(game._uid + 1)

    @staticmethod
    def test_entity_has(game, entity):
        assert not game.entity_has(entity, Health)
        assert not game.entity_has(entity, Health, Velocity)

        game.add_component_to_entity(Health(), entity)
        assert game.entity_has(entity, Health)

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
        assert velocity_component not in game._components[Velocity]

        game.add_component_to_entity(health_component, entity)
        assert game.entity_has(entity, Health)
        assert health_component in game._components[Health]

        game.add_component_to_entity(velocity_component, entity)
        assert game.entity_has(entity, Velocity)
        assert velocity_component in game._components[Velocity]

    @staticmethod
    def test_remove_component_from_entity(game, entity):
        health_component = Health()
        velocity_component = Velocity()

        game.add_component_to_entity(health_component, entity)
        game.add_component_to_entity(velocity_component, entity)

        # with pytest.raises(TypeError):
        #     game.remove_component_from_entity(Health, entity)

        game.remove_component_from_entity(Velocity, entity)
        assert not game.entity_has(entity, Velocity)
        assert velocity_component not in game._components[Velocity]

        game.remove_component_from_entity(Health, entity)
        assert not game.entity_has(entity, Health)
        assert health_component not in game._components[Health]

    @staticmethod
    def test_get_components_of_type(game, entity):
        pass
