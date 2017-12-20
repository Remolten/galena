import pytest

from .component_classes import *


def test_component_default_arguments():
    default_health_component = Health()
    default_velocity_component = Velocity()
    default_shield_component = Shield()

    assert default_health_component.entity == 0
    assert default_velocity_component.entity == 0
    assert default_shield_component.entity == 0

    assert not default_health_component.required_by
    assert not default_velocity_component.required_by
    assert not default_shield_component.required_by

    assert not default_health_component.required_components
    assert Health in default_velocity_component.required_components
    assert Health in default_shield_component.required_components
    assert Velocity in default_shield_component.required_components

    assert default_health_component.health == 1
    assert default_velocity_component.speed == 10
    assert default_velocity_component.direction == 180
    assert default_shield_component.value == 10

    not_default_health_component = Health(health=2)
    not_default_velocity_component = Velocity(speed=20, direction=0)
    not_default_shield_component = Shield(value=11)

    assert not_default_health_component.entity == 0
    assert not_default_velocity_component.entity == 0
    assert not_default_shield_component.entity == 0

    assert not not_default_health_component.required_by
    assert not not_default_velocity_component.required_by
    assert not not_default_shield_component.required_by

    assert not not_default_health_component.required_components
    assert Health in not_default_velocity_component.required_components
    assert Health in not_default_shield_component.required_components
    assert Velocity in not_default_shield_component.required_components

    assert not_default_health_component.health == 2
    assert not_default_velocity_component.speed == 20
    assert not_default_velocity_component.direction == 0
    assert not_default_shield_component.value == 11


def test_add_component_to_entity(game, entity, entity2, entity3):
    health_component = Health()
    health_component2 = Health()
    health_component3 = Health()
    velocity_component = Velocity()
    velocity_component3 = Velocity()
    shield_component3 = Shield()

    with pytest.raises(TypeError):
        game.add_component_to_entity(velocity_component, entity)
    assert not game.entity_has(entity, Velocity)
    assert velocity_component not in game.components[Velocity]

    game.add_component_to_entity(health_component2, entity2)
    assert game.entity_has(entity2, Health)
    assert health_component2 == game.components[Health][entity2]
    assert not health_component2.required_by
    assert health_component2.entity == entity2

    game.add_component_to_entity(health_component, entity)
    assert game.entity_has(entity, Health)
    assert health_component == game.components[Health][entity]
    assert not health_component.required_by
    assert health_component.entity == entity

    with pytest.raises(TypeError):
        game.add_component_to_entity(health_component, entity)

    game.add_component_to_entity(velocity_component, entity)
    assert game.entity_has(entity, Velocity)
    assert velocity_component == game.components[Velocity][entity]
    assert Velocity in health_component.required_by
    assert velocity_component.entity == entity

    game.add_component_to_entity(health_component3, entity3)
    assert game.entity_has(entity3, Health)
    assert health_component3 == game.components[Health][entity3]
    assert not health_component3.required_by
    assert health_component3.entity == entity3

    game.add_component_to_entity(velocity_component3, entity3)
    assert game.entity_has(entity3, Velocity)
    assert velocity_component3 == game.components[Velocity][entity3]
    assert Velocity in health_component3.required_by
    assert velocity_component3.entity == entity3

    game.add_component_to_entity(shield_component3, entity3)
    assert game.entity_has(entity3, Shield)
    assert shield_component3 == game.components[Shield][entity3]
    assert Shield in health_component3.required_by
    assert Shield in velocity_component3.required_by
    assert shield_component3.entity == entity3


def test_remove_component_from_entity(game, entity, entity2, entity3):
    health_component = Health()
    health_component2 = Health()
    health_component3 = Health()
    velocity_component = Velocity()
    velocity_component3 = Velocity()
    shield_component3 = Shield()

    with pytest.raises(ValueError):
        game.remove_component_from_entity(Health, entity)

    game.add_component_to_entity(health_component, entity)
    game.add_component_to_entity(velocity_component, entity)
    game.add_component_to_entity(health_component2, entity2)
    game.add_component_to_entity(health_component3, entity3)
    game.add_component_to_entity(velocity_component3, entity3)
    game.add_component_to_entity(shield_component3, entity3)

    with pytest.raises(TypeError):
        game.remove_component_from_entity(Health, entity)

    game.remove_component_from_entity(Velocity, entity)
    assert not game.entity_has(entity, Velocity)
    assert velocity_component not in game.components[Velocity].values()

    game.remove_component_from_entity(Health, entity)
    assert not game.entity_has(entity, Health)
    assert health_component not in game.components[Health].values()

    with pytest.raises(TypeError):
        game.remove_component_from_entity(Velocity, entity3)

    game.remove_component_from_entity(Shield, entity3)
    assert not game.entity_has(entity3, Shield)
    assert shield_component3 not in game.components[Shield].values()

    game.remove_component_from_entity(Velocity, entity3)
    assert not game.entity_has(entity3, Velocity)
    assert velocity_component3 not in game.components[Velocity].values()

    game.remove_component_from_entity(Health, entity3)
    assert not game.entity_has(entity3, Health)
    assert health_component3 not in game.components[Health].values()

    game.remove_component_from_entity(Health, entity2)
    assert not game.entity_has(entity2, Health)
    assert health_component2 not in game.components[Health].values()


def test_get_components_of_type(game, entity, entity2, entity3):
    health_component = Health()
    health_component2 = Health()
    health_component3 = Health()
    velocity_component = Velocity()
    velocity_component3 = Velocity()
    shield_component3 = Shield()

    game.add_component_to_entity(health_component, entity)
    game.add_component_to_entity(velocity_component, entity)
    game.add_component_to_entity(health_component2, entity2)
    game.add_component_to_entity(health_component3, entity3)
    game.add_component_to_entity(velocity_component3, entity3)
    game.add_component_to_entity(shield_component3, entity3)

    health_components = list(game.get_components_of_type(Health))
    assert health_component in health_components
    assert health_component2 in health_components
    assert health_component3 in health_components
    assert velocity_component not in health_components
    assert velocity_component3 not in health_components
    assert shield_component3 not in health_components

    velocity_components = list(game.get_components_of_type(Velocity))
    assert velocity_component in velocity_components
    assert velocity_component3 in velocity_components
    assert health_component not in velocity_components
    assert health_component2 not in velocity_components
    assert health_component3 not in velocity_components
    assert shield_component3 not in velocity_components

    shield_components = list(game.get_components_of_type(Shield))
    assert shield_component3 in shield_components
    assert health_component not in shield_components
    assert health_component2 not in shield_components
    assert health_component3 not in shield_components
    assert velocity_component not in shield_components
    assert velocity_component3 not in shield_components


def test_get_components_for_entity(game, entity, entity2, entity3):
    health_component = Health()
    health_component2 = Health()
    health_component3 = Health()
    velocity_component = Velocity()
    velocity_component3 = Velocity()
    shield_component3 = Shield()

    game.add_component_to_entity(health_component, entity)
    game.add_component_to_entity(velocity_component, entity)
    game.add_component_to_entity(health_component2, entity2)
    game.add_component_to_entity(health_component3, entity3)
    game.add_component_to_entity(velocity_component3, entity3)
    game.add_component_to_entity(shield_component3, entity3)

    health_component_for_entity = list(game.get_components_for_entity(entity, Health))
    assert health_component in health_component_for_entity
    assert health_component2 not in health_component_for_entity
    assert health_component3 not in health_component_for_entity
    assert velocity_component not in health_component_for_entity
    assert velocity_component3 not in health_component_for_entity
    assert shield_component3 not in health_component_for_entity

    velocity_component_for_entity = list(game.get_components_for_entity(entity, Velocity))
    assert velocity_component in velocity_component_for_entity
    assert health_component not in velocity_component_for_entity
    assert health_component2 not in velocity_component_for_entity
    assert health_component3 not in velocity_component_for_entity
    assert velocity_component3 not in velocity_component_for_entity
    assert shield_component3 not in velocity_component_for_entity

    shield_component_for_entity = list(game.get_components_for_entity(entity3, Shield))
    assert shield_component3 in shield_component_for_entity
    assert health_component not in shield_component_for_entity
    assert health_component2 not in shield_component_for_entity
    assert health_component3 not in shield_component_for_entity
    assert velocity_component not in shield_component_for_entity
    assert velocity_component3 not in shield_component_for_entity

    multiple_components_for_entity = list(game.get_components_for_entity(entity, Health, Velocity))
    assert health_component in multiple_components_for_entity
    assert velocity_component in multiple_components_for_entity
    assert health_component2 not in multiple_components_for_entity
    assert health_component3 not in multiple_components_for_entity
    assert velocity_component3 not in multiple_components_for_entity
    assert shield_component3 not in multiple_components_for_entity
