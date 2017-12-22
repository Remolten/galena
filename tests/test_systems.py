from .component_classes import Health, Velocity, Shield
from .system_functions import health_system, velocity_system


def test_systems(game, entity, entity2, entity3):
    game.add_component_to_entity(Health(), entity)
    game.add_component_to_entity(Velocity(), entity)
    game.add_component_to_entity(Health(), entity2)
    game.add_component_to_entity(Health(), entity3)
    game.add_component_to_entity(Velocity(), entity3)
    game.add_component_to_entity(Shield(), entity3)

    game.add_system(health_system)
    game.add_system(velocity_system)

    for _ in range(11):
        game.process()

    assert game.get_a_component_for_entity(entity, Health).health != 1
    assert game.get_a_component_for_entity(entity, Velocity).speed != 10
    assert game.get_a_component_for_entity(entity, Velocity).direction != 180
    assert game.get_a_component_for_entity(entity2, Health).health != 1
    assert game.get_a_component_for_entity(entity3, Health).health != 1
    assert game.get_a_component_for_entity(entity3, Velocity).speed != 10
    assert game.get_a_component_for_entity(entity3, Velocity).direction != 180
    assert game.get_a_component_for_entity(entity3, Shield).value != 10
