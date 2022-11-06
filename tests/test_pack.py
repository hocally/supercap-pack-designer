import unittest
from pack_builder.capacitor import Capacitor
from pack_builder.pack import Pack


class TestPack(unittest.TestCase):
    def test_pack_complete(self):
        """
        Ensure that pack parameters are computed properly
        """
        test_capacitor = Capacitor(1.0, 1.0, 1.0, "Test-Capacitor", 1.0)
        test_pack = Pack(1.0, 1.0, test_capacitor)
        self.assertEqual(test_pack.num_series_capacitors, int(1))
        self.assertEqual(test_pack.get_stack_voltage(), test_capacitor.voltage_rating)
        self.assertEqual(
            test_pack.get_stack_max_energy(), test_capacitor.get_max_energy()
        )
        self.assertEqual(test_pack.get_pack_max_energy(), float(1.0))
        self.assertEqual(test_pack.get_pack_price(), float(2.0))


if __name__ == "__main__":
    unittest.main()
