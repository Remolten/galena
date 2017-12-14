import pytest

from ..src import galena


class Health(galena.Component):
    health = 1


class Velocity(galena.Component):
    required_components = (Health,)

    speed = 10
    direction = 180


class TestGalena:
    @staticmethod
    def test_reset():
        test_galena = galena.Galena()
        test_entity = test_galena.create_entity()

        test_galena.add_component_to_entity(Health(), test_entity)

        test_galena.reset()

        assert len(test_galena._entities) == 0
        assert len(test_galena._components) == 0


class TestEntity:
    @staticmethod
    def test_create_entity():
        test_galena = galena.Galena()
        test_entity = test_galena.create_entity()

        assert test_entity == test_galena._uid

    @staticmethod
    def test_entity_exists():
        test_galena = galena.Galena()
        test_entity = test_galena.create_entity()

        assert test_galena.entity_exists(test_entity)
        assert not test_galena.entity_exists(test_galena._uid + 1)

    @staticmethod
    def test_remove_entity():
        test_galena = galena.Galena()
        test_entity = test_galena.create_entity()

        assert test_galena.remove_entity(test_entity)
        assert not test_galena.entity_exists(test_entity)
        assert not test_galena.remove_entity(test_galena._uid + 1)

    @staticmethod
    def test_entity_has():
        test_galena = galena.Galena()
        test_entity = test_galena.create_entity()

        assert not test_galena.entity_has(test_entity, (Health,))
        assert not test_galena.entity_has(test_entity, (Health, Velocity))

        test_galena.add_component_to_entity(Health(), test_entity)
        assert test_galena.entity_has(test_entity, (Health,))

        test_galena.add_component_to_entity(Velocity(), test_entity)
        assert test_galena.entity_has(test_entity, (Health, Velocity))

    @staticmethod
    def test_entities_with():
        pass


class TestComponents:
    @staticmethod
    def test_add_component_to_entity():
        test_galena = galena.Galena()
        test_entity = test_galena.create_entity()

        test_health_component = Health()
        test_velocity_component = Velocity()

        assert test_velocity_component not in test_galena._components[Velocity]

        with pytest.raises(TypeError):
            test_galena.add_component_to_entity(test_velocity_component, test_entity)  # noqa: E501

        test_galena.add_component_to_entity(test_health_component, test_entity)
        assert test_health_component in test_galena._components[Health]

        test_galena.add_component_to_entity(test_velocity_component, test_entity)  # noqa: E501
        assert test_velocity_component in test_galena._components[Velocity]
