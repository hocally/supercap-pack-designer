class Capacitor:
    def __init__(
        self,
        capacitance: float,
        voltage_rating: float,
        price: float,
        part_number,
        area: float,
    ):
        self.capacitance: float = capacitance
        self.voltage_rating: float = voltage_rating
        self.price: float = price
        self.part_number = part_number
        self.area = area

    def get_max_energy(self):
        return 0.5 * self.capacitance * self.voltage_rating**2
