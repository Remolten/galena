from collections import defaultdict
from functools import partial


class Component(object):
    required_components = ()

    def __init__(self, **aspects):
        self.required_by = []

        for aspect_name, aspect_value in aspects.items():
            if aspect_name not in self.__class__.__dict__:
                raise AttributeError('{0} does not contain an attribute named {1}. To fix this error, add an attribute named {1} to the {0} component class.'  # noqa: E501
                                     .format(self.__class__.__name__,
                                             aspect_name))
            self.__class__.__dict__[aspect_name] = aspect_value


class Game:
    def __init__(self):
        self.uid = 0

        self.entities = {}
        self.components = defaultdict(partial(defaultdict, Component))

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
            raise

        return True

    def entity_has(self, entity, *component_types):
        entity_component_types = (component for component in
                                  self.entities[entity] if component in
                                  component_types)

        for component_type in component_types:
            if component_type not in entity_component_types:
                return False

        return True

    def entities_with(self, *component_types):
        for component_type in component_types:
            for entity in self.components[component_type].keys():
                yield entity

    def add_component_to_entity(self, component, entity):
        if self.entity_has(entity, type(component)):
            raise TypeError('Cannot add component. The entity already contains a {} component.'  # noqa: E501
                            .format(type(component)))
        elif not self.entity_has(entity, *component.required_components):
            raise TypeError('Cannot add component. The entity does not contain the {} component, required before adding a {} component.'  # noqa: E501
                            .format(component.required_components,
                                    type(component)))
        elif component.required_components:
            for component_type in component.required_components:
                for owning_entity, dependent_component in self.components[component_type].items():  # noqa: E501
                    if owning_entity == entity:
                        dependent_component.required_by.append(type(component))

        self.entities[entity].append(type(component))
        self.components[type(component)][entity] = component

    def remove_component_from_entity(self, component_type, entity):
        for owning_entity, component in self.components[component_type].copy().items():  # noqa: E501
            if owning_entity == entity:
                for required_by_component_type in component.required_by:
                    if required_by_component_type in self.entities[entity]:
                        raise TypeError("Cannot remove component. The entity's {} component requires this {} component."  # noqa: E501
                                        .format(required_by_component_type,
                                                component_type))
                del self.components[component_type][entity]

        self.entities[entity].remove(component_type)

    def get_components_of_type(self, component_type):
        for component in self.components[component_type].values():
            yield component

    def get_components_for_entity(self, entity, *component_types):
        for component_type in component_types:
            yield self.components[component_type][entity]
