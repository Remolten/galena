# Copyright (c) 2016-2017, Remington Thurber
# All rights reserved.
#
# See the BSD 3-clause LICENSE file for more information.


from collections import defaultdict


def Component(cls):
    """
    This function is intended to be used as a decorator.

    It is required, and allows for nice syntax when creating components.

    Here is an example:
        @galena.Component
        class Shield:
            required_components = (Health, Velocity)

            value = 1
    """
    class WrappedClass(object):
        def __init__(self, **kwargs):
            self.entity = 0
            self.required_by = []
            self.required_components = ()

            for attribute_name, attribute_value in cls.__dict__.items():
                if attribute_name in kwargs:
                    self.__dict__[attribute_name] = kwargs[attribute_name]
                elif not attribute_name.startswith('__'):
                    self.__dict__[attribute_name] = attribute_value
    WrappedClass.__name__ = cls.__name__

    return WrappedClass


class Game(object):
    """
    The Game class manages all entities, components, and systems.

    Entities are unique ints, tracked by self.uid.

    self.entities is a dict, structured like so:
        {entity: component_type}
    For example:
        {0: [type(Health)], 2: [type(Health), type(Velocity)]}

    self.components is a defaultdict, structured like so:
        {component_type: {entity: component_instance}}
    For example:
        {type(Health): {0: health_instance, 1: other_health_instance}, type(Velocity): {1: velocity_instance}}

    self.systems is a list. It contains system functions that are called by Game.process().

    Each system function must accept one argument, the Game instance.
    """
    def __init__(self):
        self.uid = 0

        self.entities = {}
        self.components = defaultdict(dict)
        self.systems = []

    def reset(self):
        self.uid = 0

        self.entities.clear()
        self.components.clear()

    def create_entity(self):
        self.uid += 1

        self.entities[self.uid] = []

        return self.uid

    def remove_entity(self, entity):
        try:
            del self.entities[entity]
        except KeyError:
            raise KeyError('Cannot remove entity. The entity does not exist.')

    def entity_has(self, entity, *component_types):
        entity_component_types = (component for component in
                                  self.entities[entity] if component in
                                  component_types)

        for component_type in component_types:
            if component_type not in entity_component_types:
                return False

        return True

    def entities_with(self, *component_types):
        entity_occurences = defaultdict(int)
        amount_component_types = len(component_types)

        for component_type in component_types:
            for entity in self.components[component_type].keys():
                entity_occurences[entity] += 1

        for entity, frequency in entity_occurences.items():
            if frequency == amount_component_types:
                yield entity

    def add_component_to_entity(self, component, entity):
        if self.entity_has(entity, type(component)):
            raise TypeError('Cannot add component. The entity already contains a {0} component.'.format(type(component)))
        elif not self.entity_has(entity, *component.required_components):
            raise TypeError('Cannot add component. The entity does not contain the {0} component, required before adding a {1} component.'
                            .format(component.required_components, type(component)))
        elif component.required_components:
            for component_type in component.required_components:
                for owning_entity, dependent_component in self.components[component_type].items():
                    if owning_entity == entity:
                        dependent_component.required_by.append(type(component))

        component.entity = entity

        self.entities[entity].append(type(component))
        self.components[type(component)][entity] = component

    def remove_component_from_entity(self, component_type, entity):
        for owning_entity, component in self.components[component_type].copy().items():
            if owning_entity == entity:
                for required_by_component_type in component.required_by:
                    if required_by_component_type in self.entities[entity]:
                        raise TypeError("Cannot remove component. The entity's {0} component requires this {1} component."
                                        .format(required_by_component_type, component_type))
                del self.components[component_type][entity]

        try:
            self.entities[entity].remove(component_type)
        except ValueError:
            raise ValueError('Cannot remove component. The entity does not contain a {0} component'.format(component_type))

    def get_components_of_type(self, component_type):
        for component in self.components[component_type].values():
            yield component

    def get_a_component_for_entity(self, entity, component_type):
        try:
            return self.components[component_type][entity]
        except KeyError:
            return None

    def get_components_for_entity(self, entity, *component_types):
        for component_type in component_types:
            yield self.get_a_component_for_entity(entity, component_type)

    def add_system(self, system):
        self.systems.append(system)

    def process(self):
        for system in self.systems:
            system(self)
