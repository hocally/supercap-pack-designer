"""Sandbox"""
from capacitor_finder.query_tool import QueryTool
from pack_optimizer.pack_selector import PackSelector
from pack_optimizer.doe import Sweep

DESIGN_VOLTAGE = 50
DESIGN_ENERGY = 6000


def watt_hours_to_joules(watt_hours: float) -> float:
    """Helper function for quick energy conversion"""
    return watt_hours * 3600


sleuth = QueryTool(50, True)
capacitors = sleuth.capacitors_found
packs = []
for capacitor in capacitors:
    sweep = Sweep(
        DESIGN_VOLTAGE,
        DESIGN_ENERGY,
        capacitor,
        Sweep.SweepParameters(200, 5, Sweep.SweepParameters.SweepType.VOLTAGE),
    )
    sweep.enumerate_packs()
    packs.extend(sweep.packs)

#     print(pack.get_pack_report())


decider = PackSelector(packs)
print("Cheapo:")
print(decider.select_pack(PackSelector.FitnessFunction.PRICE).get_pack_report())
print("Bang for buck:")
print(
    decider.select_pack(PackSelector.FitnessFunction.PRICE_PER_ENERGY).get_pack_report()
)
print("Packaging king:")
print(
    decider.select_pack(PackSelector.FitnessFunction.AREA_PER_ENERGY).get_pack_report()
)
