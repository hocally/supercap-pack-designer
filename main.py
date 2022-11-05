from pack_builder.pack import Pack
from pack_builder.capacitor import Capacitor

test_cap = Capacitor(1.0, 2.7, 1.07)
print("Max energy: " + str(test_cap.get_max_energy()))

test_pack = Pack(40.0, 300, test_cap)
test_pack.set_num_series_capacitors(test_pack.max_voltage_goal)
print("Series capacitors: " + str(test_pack.num_series_capacitors))
print("Stack voltage: " + str(test_pack.get_stack_voltage()))
print("Stack energy: " + str(test_pack.get_stack_max_energy()))
test_pack.set_num_parallel_stacks(test_pack.min_energy_goal)
print("Pack energy: " + str(test_pack.get_pack_max_energy()))
print("Pack price: " + str(test_pack.get_pack_price()))