"""Tool using Digikey API to find capacitors to build packs from"""
import re
import math
import os
import digikey
import numpy as np
from digikey.v3.productinformation import KeywordSearchRequest
from pack_builder.capacitor import Capacitor


class QueryTool:
    """Hits Digikey API and exports capacitor data into normalized model"""

    def __init__(self, num_capacitors: int):
        self.num_capacitors = num_capacitors
        self.capacitors_found = self.search_the_information_superhighway()

    def only_numerics(self, seq):
        """Strip out non-numeric characters"""

        seq_type = type(seq)
        return seq_type().join(filter(seq_type.isdigit, seq))

    def create_cap_object(
        self, capacitor_data_raw, capacitor_price_raw, manufacturer_part_number
    ) -> Capacitor:
        """Creates capacitor model from API data"""
        # pylint: disable=too-many-locals

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
                            re.sub(r"[^\d\.]", "", parameter["value"])
                        )
                    case "Capacitance":
                        capacitance = float(re.sub(r"[^\d\.]", "", parameter["value"]))
                        if "m" in parameter["value"]:
                            capacitance /= 1000
                    case "Size / Dimension":
                        if "x" in parameter["value"]:
                            area = parameter["value"]
                            area = area[area.find("(") + 1 : area.find(")")]
                            length = float(area[0 : area.find("m")])
                            width_space = area[area.find("m") : -1]
                            width_anchor = re.search(r"\d", width_space)
                            assert width_anchor is not None
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
                            circle_area = float(re.sub(r"[^\d\.]", "", circle_area))
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

    def generate_value_list(self, min, max) -> list[dict]:
        out = []
        for i in range(min, max):
            out.append(
                {"ParameterId": 2049, "ValueId": str(i)},
            )
        return out

    def generate_voltage_list(self, min, max) -> list[dict]:
        out = []
        for i in np.arange(min, max, 0.01):
            out.append(
                {"ParameterId": 2079, "ValueId": str(i)},
            )
        return out

    def search_the_information_superhighway(self) -> list[Capacitor]:
        """Hackerman.wav"""

        # Search for parts
        search_request = KeywordSearchRequest(
            keywords="capacitor",
            record_count=self.num_capacitors,
            filters={
                "TaxonomyIds": [61],
                "ParametricFilters": [
                    {"ParameterId": 1989, "ValueId": "0"},
                    # {"ParameterId": 69, "ValueId": "411897"},
                    # {"ParameterId": 69, "ValueId": "409393"},
                    # {"ParameterId": -1, "ValueId": "1572"},
                    # {"ParameterId": -1, "ValueId": "338"},
                ]
                + self.generate_value_list(120, 1000)
                + self.generate_voltage_list(1, 9),
            },
        )

        api_limit = {}
        result = digikey.keyword_search(body=search_request, api_limits=api_limit)

        print(api_limit)
        # print(result)

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
