"""Structure to build packs from capacitor models"""
import math
from pack_builder.capacitor import Capacitor


class Pack:
    """A capacitor pack. Constructs and computes pack information"""

    def __init__(
        self, max_voltage_goal: float, min_energy_goal: float, capacitor: Capacitor
    ):
        self.max_voltage_goal: float = max_voltage_goal
        self.min_energy_goal: float = min_energy_goal
        self.capacitor = capacitor
        self.num_series_capacitors: int = 0
        self.num_parallel_stacks: int = 0
        self.set_num_series_capacitors()
        self.set_num_parallel_stacks()

    def set_num_series_capacitors(self):
        """Compute and set number of capacitors in a stack"""
        self.num_series_capacitors = math.floor(
            self.max_voltage_goal / self.capacitor.voltage_rating
        )

    def get_stack_max_energy(self) -> float:
        """Compute energy stored in a stack"""
        assert (
            self.num_series_capacitors != 0
        ), "Cannot compute stack energy without stack size defined!"
        series_capacitance = 1 / (
            self.num_series_capacitors * (1 / self.capacitor.capacitance)
        )
        return (
            0.5
            * series_capacitance
            * (self.capacitor.voltage_rating * self.num_series_capacitors) ** 2
        )

    def get_stack_voltage(self) -> float:
        """Compute voltage of stack"""
        assert (
            self.num_series_capacitors != 0
        ), "Cannot compute stack voltage without stack size defined!"
        return self.num_series_capacitors * self.capacitor.voltage_rating

    def set_num_parallel_stacks(self):
        """Compute and set number of capacitors in a stack"""
        self.num_parallel_stacks = math.ceil(
            self.min_energy_goal / self.get_stack_max_energy()
        )

    def get_pack_max_energy(self) -> float:
        """Compute energy in entire pack"""
        assert (
            self.num_parallel_stacks is not None
        ), "Cannot compute pack energy without number of stacks defined!"
        return self.get_stack_max_energy() * self.num_parallel_stacks

    def get_num_capacitors(self) -> int:
        """Compute number of capacitors in stack"""
        assert (
            self.num_series_capacitors is not None
            and self.num_parallel_stacks is not None
        ), "Pack must be defined before number of capacitors used is calculated!"
        return self.num_series_capacitors * self.num_parallel_stacks

    def get_pack_price(self) -> float:
        """Compute price of pack"""
        assert (
            self.num_series_capacitors is not None
            and self.num_parallel_stacks is not None
        ), "Pack must be defined before price is calculated!"
        return self.get_num_capacitors() * self.capacitor.price

    def get_pack_area(self) -> float:
        """Compute area of pack"""
        assert (
            self.num_series_capacitors is not None
            and self.num_parallel_stacks is not None
        ), "Pack must be defined before area is calculated!"
        if self.capacitor.area is not None:
            return self.get_num_capacitors() * self.capacitor.area
        return float("NaN")

    def get_pack_joules_per_dollar(self) -> float:
        """Compute energy per dollar of pack"""
        return self.get_pack_max_energy() / self.get_pack_price()

    def get_pack_joules_per_area(self):
        """Compute energy per area of pack"""
        assert (
            self.num_series_capacitors is not None
            and self.num_parallel_stacks is not None
        ), "Pack must be defined before area things can be calculated!"
        if not math.isnan(self.get_pack_area()):
            return self.get_pack_max_energy() / self.get_pack_area()  # type: ignore
        return None

    def get_pack_report(self):
        """Return a string representing data about the pack"""
        return (
            str(f"{self.get_stack_voltage():.3f}")
            + " V, "
            + str(f"{self.get_pack_max_energy():.3f}")
            + " J, $"
            + str(f"{self.get_pack_price():.3f}")
            + ", "
            + str(f"{self.get_pack_joules_per_dollar():.3f}")
            + " J/$: "
            + str(f"{self.get_pack_joules_per_area():.3f}")
            + " J/sq mm, "
            + str(self.capacitor.part_number)
        )
