import unittest
from pack_builder.capacitor import Capacitor


class TestCapacitor(unittest.TestCase):
    def test_capacitor_energy(self):
        """
        Ensure that capacitors compute energy correctly
        """
        test_capacitor = Capacitor(1.0, 1.0, 1.0)
        energy = test_capacitor.get_max_energy()
        self.assertEqual(energy, 0.5)

        test_capacitor = Capacitor(1.0, 2.0, 1.0)
        energy = test_capacitor.get_max_energy()
        self.assertEqual(energy, 2.0)


if __name__ == "__main__":
    unittest.main()
