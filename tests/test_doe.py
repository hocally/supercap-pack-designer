"""Tests for DOE Tools"""
import unittest
from pack_optimizer.doe import Sweep
from pack_builder.capacitor import Capacitor


class TestSweep(unittest.TestCase):
    """Sweep tester"""

    def test_sweep(self):
        """
        Ensure sweeps aren't sus
        """
        test_capacitor = Capacitor(1.0, 1.0, 1.0, "Test-Capacitor-1", 1.0)
        test_sweep = Sweep(
            1.0,
            1.0,
            test_capacitor,
            Sweep.SweepParameters(10, 1, Sweep.SweepParameters.SweepType.VOLTAGE),
        )
        assert isinstance(test_sweep, Sweep)


if __name__ == "__main__":
    unittest.main()
