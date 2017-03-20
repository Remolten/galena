from collections import defaultdict


class Component(object):
    def __init__(self, id_, requires=()):
        self.id_ = id_
        self.parent_entity = 0
        self.requires = requires

    @property
    def id(self):
        return self.id_


class Galena(object):
    def __init__(self):
        self.uid = 0

        self.entities = {}
        self.components = defaultdict(list)

    def create_entity(self):
        self.uid += 1
        self.entities[self.uid] = []

        return self.uid

    def entity_exists(self, entity):
        if entity in self.entities:
            return True

        return False

    def remove_entity(self, entity):
        try:
            # This should delete component references and add them to the
            # component pool as well
            del self.entities[entity]
        except KeyError:
            raise KeyError('Could not remove requested entity. Entity not found.')  # noqa: E501

    # FIXME This needs to be renamed, and component_types should just be a list
    def entity_has(self, entity, *component_types):
        entity_component_types = [type(component) for component in
                                  self.entities[entity]]

        for component_type in component_types:
            if component_type not in entity_component_types:
                return False

        return True

    '''def entities_with(self, *component_types):
        for component_type in component_types:
            for component in self.components_of_type(component_type):
                yield self.entities[component.parent_entity]'''

    def add_component_to(self, entity, component):
        if not entity.has(*component.requires):
            raise NotImplementedError('Cannot add component. The entity does not implement the component {0} required by {1}'  # noqa: E501
                                      .format(component.requires,
                                              type(component)))

        component.parent_entity = entity
        self.components[type(component)].append(component)

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
