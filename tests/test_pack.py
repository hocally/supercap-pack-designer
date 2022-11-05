import unittest
from pack_builder.capacitor import Capacitor
from pack_builder.pack import Pack

class TestPack(unittest.TestCase):
    def test_pack_complete(self):
        """
        Ensure that pack parameters are computed properly
        """
        test_cap = Capacitor(1.0, 1.0, 1.0)
        test_pack = Pack(1.0, 1.0, test_cap)

        test_pack.set_num_series_capacitors(test_pack.max_voltage_goal)
        self.assertEqual(test_pack.num_series_capacitors, int(1))
        self.assertEqual(test_pack.get_stack_voltage(), test_cap.voltage_rating)
        self.assertEqual(test_pack.get_stack_max_energy(), test_cap.get_max_energy())

        test_pack.set_num_parallel_stacks(test_pack.min_energy_goal)

        self.assertEqual(test_pack.get_pack_max_energy(), float(1.0))
        self.assertEqual(test_pack.get_pack_price(), float(2.0))

if __name__ == '__main__':
    unittest.main()