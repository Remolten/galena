import unittest
import galena


class TestEntity(unittest.TestCase):
    def get_test_galena(self):
        return galena.Galena()

    def test_create_entity(self):
        test_galena = self.get_test_galena()
        test_entity = test_galena.create_entity()

        self.assertEqual(test_entity, test_galena.uid)

    def test_remove_entity(self):
        test_galena = self.get_test_galena()
        test_entity = test_galena.create_entity()

        with self.assertRaises(KeyError):
            test_galena.remove_entity(test_galena.uid + 1)

        test_galena.remove_entity(test_entity)

        # Could replace this with an entity_exists function call
        self.assertFalse(test_entity in test_galena.entities)

'''class TestComponent(galena.Component):
    def __init__(self):
        super.__init__()


class TestComponents(unittest.TestCase):
    def get_test_component(self):
        return object()

    def test_stuff(self):
        pass'''
