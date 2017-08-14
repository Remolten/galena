from collections import defaultdict


class Component(object):
    _owning_entity = 0
    required_components = ()

    def __init__(self, **aspects):
        for aspect_name, aspect_value in aspects.items():
            if aspect_name not in self.__class__.__dict__:
                raise AttributeError('{0} does not contain an attribute named {1}. To fix this error, add an attribute named {1} to the {0} component class.'  # noqa: E501
                                     .format(self.__class__.__name__,
                                             aspect_name))
            self.__class__.__dict__[aspect_name] = aspect_value


class Galena:
    def __init__(self):
        self._uid = 0

        self._entities = {}
        self._components = defaultdict(list)

    def reset(self):
        self._uid = 0

        self._entities.clear()
        self._components.clear()

    def create_entity(self):
        self._uid += 1

        self._entities[self._uid] = []

        return self._uid

    def entity_exists(self, entity):
        if entity in self._entities:
            return True

        return False

    def remove_entity(self, entity):
        if self.entity_exists(entity):
            # TODO Delete component references and add them to the component
            # pool
            del self._entities[entity]
            return True

        return False

    def entity_has(self, entity, component_types):
        entity_component_types = (component for component in
                                  self._entities[entity] if component in
                                  component_types)

        for component_type in component_types:
            if component_type not in entity_component_types:
                return False

        return True

    def entities_with(self, component_types):
        for component_type in component_types:
            # TODO It's significantly faster to search the components, but those
            # functions are not implemented yet
            for entity in self._entities:
                if component_type in entity:
                    yield entity

    def add_component_to_entity(self, component, entity):
        if not self.entity_has(entity, component.required_components):
            raise TypeError('Cannot add component. The entity does not implement the component {0} required by {1}.'  # noqa: E501
                            .format(component.required_components,
                                    type(component)))

        component._owning_entity = entity

        self._entities[entity].append(type(component))
        self._components[type(component)].append(component)

    '''def add_components_to(self, entity, *components):
        for component in components:
            self.add_component(entity, component)

    def remove_component_from(self, entity, component):
        for component in self.components_of_type(type(component)):
            if component.parent_entity == entity.id:
                del component

    def remove_components_from(self, entity, *components):
        for component in components:
            self.remove_component(entity, component)

    def get_components(self, component_type):
        return self.components_of_type(component_type)

    def components_of_type(self, component_type):
        return self.components[component_type]'''
