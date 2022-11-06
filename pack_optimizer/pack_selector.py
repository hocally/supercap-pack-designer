"""Fitness functions and optimizers for pack selections"""
from enum import Enum
from pack_builder.pack import Pack


class PackSelector:
    """Tool for selection optimal pack"""

    # pylint: disable=too-few-public-methods

    class FitnessFunction(Enum):
        """Optimization strategy, parameter to be minimized"""

        PRICE = 0
        PRICE_PER_ENERGY = 1
        AREA_PER_ENERGY = 2

    def __init__(self, packs: list[Pack]) -> None:
        self.packs = packs

    def select_pack(self, fitness_function: FitnessFunction) -> Pack:
        """Select best pack given fitness function"""
        match fitness_function:
            case self.FitnessFunction.PRICE:
                return min(self.packs, key=lambda x: x.get_pack_price())
            case self.FitnessFunction.PRICE_PER_ENERGY:
                return min(self.packs, key=lambda x: 1 / x.get_pack_joules_per_dollar())
            case _:
                return min(self.packs, key=lambda x: 1 / x.get_pack_joules_per_area())
