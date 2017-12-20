import pytest

from .component_classes import Health, Velocity, Shield


def test_create_entity(game, entity, entity2):
    assert entity2 == game.uid
    assert entity in game.entities
    assert entity2 in game.entities


def test_remove_entity(game, entity, entity2):
    game.remove_entity(entity)
    assert entity not in game.entities

    game.remove_entity(entity2)
    assert entity2 not in game.entities

    with pytest.raises(KeyError):
        game.remove_entity(game.uid + 1)


def test_entity_has(game, entity, entity2, entity3):
    assert not game.entity_has(entity, Health)
    assert not game.entity_has(entity, Health, Velocity)

    game.add_component_to_entity(Health(), entity)
    game.add_component_to_entity(Velocity(), entity)
    game.add_component_to_entity(Health(), entity2)
    game.add_component_to_entity(Health(), entity3)
    game.add_component_to_entity(Velocity(), entity3)
    game.add_component_to_entity(Shield(), entity3)

    assert game.entity_has(entity, Health)
    assert game.entity_has(entity, Velocity)
    assert not game.entity_has(entity, Shield)
    assert game.entity_has(entity, Health, Velocity)
    assert not game.entity_has(entity, Health, Velocity, Shield)

    assert game.entity_has(entity2, Health)
    assert not game.entity_has(entity2, Velocity)
    assert not game.entity_has(entity2, Shield)
    assert not game.entity_has(entity2, Health, Velocity)
    assert not game.entity_has(entity2, Health, Velocity, Shield)

    assert game.entity_has(entity3, Health)
    assert game.entity_has(entity3, Velocity)
    assert game.entity_has(entity3, Shield)
    assert game.entity_has(entity3, Health, Velocity)
    assert game.entity_has(entity3, Health, Velocity, Shield)


def test_entities_with(game, entity, entity2, entity3):
    game.add_component_to_entity(Health(), entity)
    game.add_component_to_entity(Velocity(), entity)
    game.add_component_to_entity(Health(), entity2)
    game.add_component_to_entity(Health(), entity3)
    game.add_component_to_entity(Velocity(), entity3)
    game.add_component_to_entity(Shield(), entity3)

    health_entities = list(game.entities_with(Health))
    velocity_entities = list(game.entities_with(Velocity))
    shield_entities = list(game.entities_with(Shield))

    assert entity in health_entities
    assert entity2 in health_entities
    assert entity3 in health_entities
    assert entity in velocity_entities
    assert entity2 not in velocity_entities
    assert entity3 in velocity_entities
    assert entity not in shield_entities
    assert entity2 not in shield_entities
    assert entity3 in shield_entities

    health_velocity_entities = list(game.entities_with(Health, Velocity))

    assert entity in health_velocity_entities
    assert entity2 not in health_velocity_entities
    assert entity3 in health_velocity_entities
