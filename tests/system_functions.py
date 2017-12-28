from .component_classes import Health, Velocity, Shield


def health_system(game):
    entity_is_damaged = True

    for health_component in game.get_components(Health):
        if entity_is_damaged:
            shield_component_for_entity = game.get_a_component_for_entity(health_component.entity, Shield)

            if shield_component_for_entity is not None and shield_component_for_entity.value > 0:
                shield_component_for_entity.value -= 1
            else:
                health_component.health -= 1


def velocity_system(game):
    moving = True

    for velocity_component in game.get_components(Velocity):
        if moving:
            velocity_component.direction = 0

        velocity_component.speed += 1
