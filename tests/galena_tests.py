import unittest

try:
    import galena
except ImportError:
    from .. import galena


class TestEntity(unittest.TestCase):
    def get_test_galena(self):
        return galena.Galena()

    def get_test_entity(self, test_galena):
        return test_galena.create_entity()

    def test_create_entity(self):
        test_galena = self.get_test_galena()
        test_entity = self.get_test_entity(test_galena)

        self.assertIsInstance(test_entity, galena.Entity)
        self.assertEqual(test_galena.entities[test_entity.id],
                         test_entity)
        self.assertEqual(test_entity.id, test_galena.uid)

    def test_get_entity(self):
        test_galena = self.get_test_galena()
        test_entity = self.get_test_entity(test_galena)

        with self.assertRaises(KeyError):
            test_entity_dne = galena.Entity(test_galena.uid + 1,
                                             test_galena.entity_has)
            test_galena.get_entity(test_entity_dne.id)

        self.assertEqual(test_entity, test_galena.get_entity(test_entity.id))

    def test_remove_entity(self):
        test_galena = self.get_test_galena()
        test_entity = self.get_test_entity(test_galena)

        with self.assertRaises(KeyError):
            test_galena.remove_entity(test_galena.uid + 1)

        self.assertTrue(test_galena.remove_entity(test_entity.id))
        self.assertFalse(test_galena.entities.get(test_entity.id, False))


class TestComponents(unittest.TestCase):
    def test_stuff(self):
        pass
