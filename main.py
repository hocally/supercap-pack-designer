from pack_builder.capacitor import Capacitor
from pack_optimizer.doe import Sweep


def watt_hours_to_joules(watt_hours: float) -> float:
    return watt_hours * 3600


test_cap = Capacitor(1.0, 1.0, 1.0)
sweep_params = Sweep.SweepParameters(10, 10.0)
print(sweep_params.points)
test_sweep = Sweep(52.0, 1500, test_cap, Sweep.SweepType.ENERGY, sweep_params)
test_sweep.enumerate_packs()
