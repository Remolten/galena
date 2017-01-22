from collections import defaultdict


class Entity:
    def __init__(self, _id, entity_has_reference):
        self._id = _id
        self.entity_has_reference = entity_has_reference

    def has(self, *component_types):
        return self.entity_has_reference(self.id, *component_types)

    @property
    def id(self):
        return self._id


class Component:
    def __init__(self, _id, requires=[]):
        self._id = _id
        self.parent_entity = 0
        self.requires = requires

    @property
    def id(self):
        return self._id


class Galena:
    def __init__(self):
        self.uid = 0

        self.entities = {}
        self.components = defaultdict(list)

    def create_entity(self):
        self.uid += 1

        entity = Entity(self.uid, self.entity_has)
        self.entities[entity.id] = entity
        return entity

    def remove_entity(self, entity):
        try:
            del self.entities[entity.id]
        except KeyError:
            raise KeyError('''Could not remove requested entity. Entity not
                           found.''')

    def get_entity(self, _id):
        try:
            return self.entities[_id]
        except KeyError:
            raise KeyError('Could not find requested entity.')

    def entities_with(self, *component_types):
        for component_type in component_types:
            for component in self.components_of_type(component_type):
                yield self.entities[component.parent_entity]

    def entity_has(self, _id, *component_types):
        for component_type in component_types:
            for component in self.components_of_type(component_type):
                if component.parent_entity == _id:
                    break
            else:
                return False

        return True

    def add_component(self, entity, component):
        if not entity.has(*component.requires):
            raise NotImplementedError('''Cannot add component. The entity does
                                      not implement the components {0}
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
