import re
import os
import digikey
from digikey.v3.productinformation import KeywordSearchRequest
from pack_builder.capacitor import Capacitor
import math


class CapacitorFinder:
    def __init__(self, num_capacitors: int):
        self.num_capacitors = num_capacitors
        self.capacitors_found = self.search_the_information_superhighway()

    def only_numerics(self, seq):
        seq_type = type(seq)
        return seq_type().join(filter(seq_type.isdigit, seq))

    def create_cap_object(
        self, capacitor_data_raw, capacitor_price_raw, manufacturer_part_number
    ) -> Capacitor:
        capacitance = None
        voltage_rating = None
        price = capacitor_price_raw[0]["unit_price"]
        area = None
        for parameter in capacitor_data_raw:
            # print(parameter)
            if capacitance or voltage_rating is None:
                match parameter["parameter"]:
                    case "Voltage - Rated":
                        voltage_rating = float(
                            re.sub("[^\d\.]", "", parameter["value"])
                        )
                    case "Capacitance":
                        capacitance = float(re.sub("[^\d\.]", "", parameter["value"]))
                        if "m" in parameter["value"]:
                            capacitance /= 1000
                    case "Size / Dimension":
                        if "x" in parameter["value"]:
                            area = parameter["value"]
                            area = area[area.find("(") + 1 : area.find(")")]
                            length = float(area[0 : area.find("m")])
                            width_space = area[area.find("m") : -1]
                            width_anchor = re.search(r"\d", width_space)
                            width_space = area[width_anchor.start() : -1]
                            width = float(width_space[width_anchor.start() : -1])
                            area = length * width
                        elif parameter["value"] == "-":
                            area = None
                        else:
                            circle_area = parameter["value"]
                            circle_area = circle_area[
                                circle_area.find("(") + 1 : circle_area.find(")")
                            ]
                            circle_area = float(re.sub("[^\d\.]", "", circle_area))
                            radius = math.sqrt(circle_area / math.pi)
                            side_length = 2 * radius
                            area = side_length**2
                            # m = re.search(r"\d", area)

            else:
                break
        assert capacitance and voltage_rating is not None
        return Capacitor(
            capacitance, voltage_rating, price, manufacturer_part_number, 12.0
        )

    def search_the_information_superhighway(self) -> list[Capacitor]:
        # Search for parts
        search_request = KeywordSearchRequest(
            keywords="capacitor",
            record_count=self.num_capacitors,
            filters={
                "TaxonomyIds": [61],
                "ParametricFilters": [
                    {"ParameterId": 1989, "ValueId": "0"},
                    {"ParameterId": 69, "ValueId": "411897"},
                    {"ParameterId": 69, "ValueId": "409393"},
                ],
            },
        )

        api_limit = {}
        result = digikey.keyword_search(body=search_request, api_limits=api_limit)

        caps_raw = result.to_dict()["products"]
        caps = []
        for cap in caps_raw:
            if len(cap["standard_pricing"]) > 0:
                caps.append(
                    self.create_cap_object(
                        cap["parameters"],
                        cap["standard_pricing"],
                        cap["manufacturer_part_number"],
                    )
                )
        return caps