"""Tools for DOE analysis"""

from enum import Enum
from typing import NamedTuple
import numpy as np
from pack_builder.capacitor import Capacitor
from pack_builder.pack import Pack


class Sweep:
    """Single dimension sweeper"""

    class SweepType(Enum):
        """Type of sweep"""

        VOLTAGE = 0
        ENERGY = 1

    class SweepParameters(NamedTuple):
        """Parameters for sweep"""

        points: int
        percentage: float  # Max and min percent

    def __init__(
        self,
        baseline_voltage: float,
        baseline_energy: float,
        capacitor: Capacitor,
        sweep_type: SweepType,
        sweep_parameters: SweepParameters,
    ):
        self.baseline_voltage = baseline_voltage
        self.baseline_energy = baseline_energy
        self.capacitor = capacitor
        self.sweep_type = sweep_type
        self.sweep_parameters = sweep_parameters
        self.packs = []

    def enumerate_packs(self):
        """Create packs from sweep parameters"""
        voltage_goals = []
        energy_goals = []
        match self.sweep_type:
            case self.SweepType.VOLTAGE:
                energy_goals = [self.baseline_energy] * self.sweep_parameters.points
                min_voltage = self.baseline_energy * (
                    1.0 - (self.sweep_parameters.percentage / 100)
                )
                max_voltage = self.baseline_energy * (
                    1.0 + (self.sweep_parameters.percentage / 100)
                )
                voltage_goals = np.linspace(
                    min_voltage, max_voltage, self.sweep_parameters.points
                )
            case self.SweepType.ENERGY:
                voltage_goals = [self.baseline_voltage] * self.sweep_parameters.points
                min_energy = self.baseline_energy * (
                    1.0 - (self.sweep_parameters.percentage / 100)
                )
                max_energy = self.baseline_energy * (
                    1.0 + (self.sweep_parameters.percentage / 100)
                )
                energy_goals = np.linspace(
                    min_energy, max_energy, self.sweep_parameters.points
                )

        for voltage_goal, energy_goal in zip(voltage_goals, energy_goals):
            self.packs.append(Pack(voltage_goal, energy_goal, self.capacitor))
        # print([pack.get_pack_price() for pack in self.packs])
