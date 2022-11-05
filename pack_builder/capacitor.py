class Capacitor:
    def __init__(self, capacitance: float, voltage_rating: float, price: float):
        self.capacitance: float = capacitance
        self.voltage_rating: float = voltage_rating
        self.price: float = price

    def get_max_energy(self):
        return 0.5 * self.capacitance * self.voltage_rating**2
