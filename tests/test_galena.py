from .component_classes import *


def test_reset(game, entity, entity2):
    game.add_component_to_entity(Health(), entity)
    game.add_component_to_entity(Velocity(), entity)
    game.add_component_to_entity(Health(), entity2)

    game.reset()

    assert game.uid == 0
    assert len(game.entities) == 0
    assert len(game.components) == 0
