from collections import defaultdict


class Entity(object):
    def __init__(self, id_, entity_has_reference):
        self.id_ = id_
        self.entity_has_reference = entity_has_reference

    def has(self, *component_types):
        return self.entity_has_reference(self.id, *component_types)

    @property
    def id(self):
        return self.id_


class Component(object):
    def __init__(self, id_, requires=[]):
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

        entity = Entity(self.uid, self.entity_has)
        self.entities[entity.id] = entity
        return entity

    def remove_entity(self, id_):
        try:
            del self.entities[id_]
            return True
        except KeyError:
            raise KeyError('''Could not remove requested entity. Entity not
                           found.''')

    def get_entity(self, id_):
        try:
            return self.entities[id_]
        except KeyError:
            raise KeyError('Could not find requested entity.')

    def entities_with(self, *component_types):
        for component_type in component_types:
            for component in self.components_of_type(component_type):
                yield self.entities[component.parent_entity]

    def entity_has(self, id_, *component_types):
        for component_type in component_types:
            for component in self.components_of_type(component_type):
                if component.parent_entity == id_:
                    break
            else:
                return False

        return True

    def add_component(self, entity, component):
        if not entity.has(*component.requires):
            raise NotImplementedError('''Cannot add component. The entity does
                                      not implement the component {0}
                                      required by {1}'''.format(
                                      component.requires, type(component)))

        component.parent_entity = entity
        self.components[type(component)].append(component)

    def add_components(self, entity, *components):
        for component in components:
            self.add_component(entity, component)

    def remove_component(self, entity, component):
        for component in self.components_of_type(type(component)):
            if component.parent_entity == entity.id:
                del component

    def remove_components(self, entity, *components):
        for component in components:
            self.remove_component(entity, component)

    def get_components(self, component_type):
        return self.components_of_type(component_type)

    def components_of_type(self, component_type):
        return self.components[component_type]
