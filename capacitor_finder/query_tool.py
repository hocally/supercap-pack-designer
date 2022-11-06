"""Tool using Digikey API to find capacitors to build packs from"""
import re
import os
from joblib import Parallel, delayed
import digikey
import numpy as np
from digikey.v3.productinformation import KeywordSearchRequest
from pack_builder.capacitor import Capacitor


class QueryTool:
    """Hits Digikey API and exports capacitor data into normalized model"""

    def __init__(self, num_capacitors: int, parallelism_enabled: bool):
        self.num_capacitors = num_capacitors
        results = []
        ranges = [
            (0, 1),
            (1, 5),
            (5, 10),
            (10, 20),
            (20, 40),
            (40, 60),
            (60, 100),
            (100, 200),
            (200, 500),
        ]
        if parallelism_enabled:
            results = Parallel(n_jobs=9)(
                delayed(self.process)(bottom, top) for (bottom, top) in ranges
            )
            assert isinstance(results, list)
            results = [item for sublist in results for item in sublist]
        else:
            for (bottom, top) in ranges:
                results.extend(self.process(bottom, top))

        self.capacitors_found = self.aggregate_results(results)

    def process(self, bottom, top):
        """Parallelized call"""
        (
            fresh_data,
            hits_left,
            new_parts,
        ) = self.search_the_information_superhighway(bottom, top)

        print(
            "Found "
            + str(new_parts)
            + " new parts. "
            + str(hits_left)
            + " API hits left."
        )
        return fresh_data

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
                            diameter = parameter["value"]
                            diameter = diameter[
                                diameter.find("(") + 1 : diameter.find(")")
                            ]
                            diameter = float(re.sub(r"[^\d\.]", "", diameter))
                            area = diameter**2
                            # m = re.search(r"\d", area)

            else:
                break
        assert capacitance and voltage_rating is not None
        return Capacitor(
            capacitance, voltage_rating, price, manufacturer_part_number, area
        )

    def generate_value_list(self, min_value: int, max_value: int) -> list[dict]:
        """Generates list of allowable capacitances"""
        out = []
        for i in range(min_value, max_value):
            out.append(
                {"ParameterId": 2049, "ValueId": str(i) + " F"},
            )
        return out

    def generate_value_list_millifarad(self) -> list[dict]:
        """Generates list of allowable capacitances"""
        out = []
        for i in range(100, 999):
            out.append(
                {"ParameterId": 2049, "ValueId": str(i) + " mF"},
            )
        return out

    def generate_voltage_list(
        self, min_voltage: float, max_voltage: float
    ) -> list[dict]:
        """Generates list of allowable voltages"""
        out = []
        for i in np.arange(min_voltage, max_voltage, 0.01):
            out.append(
                {"ParameterId": 2079, "ValueId": str(i)},
            )
        return out

    def search_the_information_superhighway(
        self, min_capacitance, max_capacitance
    ) -> tuple[list[Capacitor], int, int]:
        """Hackerman.wav"""
        os.environ["DIGIKEY_CLIENT_ID"] = "G6vI4E0UNkg20b4gbTLm26UlLHufpuoz"
        os.environ["DIGIKEY_CLIENT_SECRET"] = "2DkKtCGaPfFwJt4N"
        os.environ["DIGIKEY_CLIENT_SANDBOX"] = "False"
        os.environ["DIGIKEY_STORAGE_PATH"] = os.path.join(os.getcwd(), "cache")

        if min_capacitance == 0:
            capacitance_list: list[dict] = self.generate_value_list_millifarad()
        else:
            capacitance_list: list[dict] = self.generate_value_list(
                min_capacitance, max_capacitance
            )

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
                + self.generate_voltage_list(1, 9)
                + capacitance_list,
            },
        )

        api_limit = {}
        result = digikey.keyword_search(body=search_request, api_limits=api_limit)

        hits_left: int = api_limit["api_requests_remaining"]
        # print(result)
        return (
            result.to_dict()["products"],
            hits_left,
            len(result.to_dict()["products"]),
        )

    def aggregate_results(self, caps_raw):
        """Aggregate queries"""
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
