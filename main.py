from pack_builder.pack import Pack
from capacitor_finder.query_tool import CapacitorFinder


def watt_hours_to_joules(watt_hours: float) -> float:
    return watt_hours * 3600


sleuth = CapacitorFinder(50)
capacitors = sleuth.capacitors_found
packs = []
for capacitor in capacitors:
    packs.append(Pack(50, 5000, capacitor))

for pack in packs:
    print(pack.get_pack_report())
