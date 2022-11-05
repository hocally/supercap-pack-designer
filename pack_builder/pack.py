from pack_builder.capacitor import Capacitor
import math

class Pack:
	def __init__(self, voltage_goal: float, energy_goal: float, capacitor: Capacitor):
		self.max_voltage_goal: float = voltage_goal
		self.min_energy_goal: float = energy_goal
		self.capacitor = capacitor
		self.num_series_capacitors: int = None
		self.num_parallel_stacks: int = None
	
	def set_num_series_capacitors(self, max_voltage) -> int:
		self.num_series_capacitors = math.floor(max_voltage / self.capacitor.voltage_rating)

	def get_stack_max_energy(self) -> float:
		assert self.num_series_capacitors is not None, "Cannot compute stack energy without stack size defined!"
		series_capacitance = 1 / (self.num_series_capacitors * (1 / self.capacitor.capacitance))
		return 0.5 * series_capacitance * (self.capacitor.voltage_rating * self.num_series_capacitors) ** 2
	
	def get_stack_voltage(self) -> float:
		assert self.num_series_capacitors is not None, "Cannot compute stack voltage without stack size defined!"
		return self.num_series_capacitors * self.capacitor.voltage_rating

	def set_num_parallel_stacks(self, min_energy):
		self.num_parallel_stacks = math.ceil(min_energy / self.get_stack_max_energy())

	def get_pack_max_energy(self) -> float:
		assert self.num_parallel_stacks is not None, "Cannot compute pack energy without number of stacks defined!"
		return self.get_stack_max_energy() * self.num_parallel_stacks

	def get_num_capacitors(self) -> int:
		assert self.num_series_capacitors is not None and self.num_parallel_stacks is not None, "Pack must be defined before number of capacitors used is calculated!"
		return self.num_series_capacitors * self.num_parallel_stacks

	def get_pack_price(self) -> float:
		assert self.num_series_capacitors is not None and self.num_parallel_stacks is not None, "Pack must be defined before number of capacitors used is calculated!"
		return self.get_num_capacitors() * self.capacitor.price