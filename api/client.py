import json
# from api import *
from api.utils import join_path
from api.settings import *
from api.split_data import get_disruptions, get_lines
import pandas as pd
import requests
import csv


class NavitiaClient:
    def __init__(self):
        self.headers: dict = HEADERS
        self.url_base: str = URL_BASE
        self.lines_endp: str = URL_BASE + "physical_modes/physical_mode:sample" + LINES_ENDPOINT
        self.journeys_endp: str = URL_BASE + "physical_modes/physical_mode:sample" + JOURNEYS_ENDPOINT
        print()
        print(self.lines_endp)

    def factor_data(self, transport_mode):
        uurl = self.lines_endp.replace("sample", transport_mode)
        print()
        print(uurl)

        response = requests.get(uurl, headers=self.headers).json()
        disruptions = response["disruptions"]
        lines = response["lines"]
        df_disruptions = get_disruptions(disruptions)
        df_lines = get_lines(lines)

        return df_disruptions, df_lines

    def df_to_csv(self, df_disruptions, df_lines, disruptions_file, lines_file):
        path = join_path("..", "data", "navitia")
        disruptions_path = join_path(path, disruptions_file)
        lines_path = join_path(path, lines_file)
        df_disruptions.to_csv(disruptions_path, index=False, sep=";")
        df_lines.to_csv(lines_path, index=False, sep=";")

    def get_all_Metro_lines_json(self):
        df_disruptions, df_lines = self.factor_data("Metro")
        self.df_to_csv(
            df_disruptions,
            df_lines,
            join_path("metros", "disruptions_metros.csv"),
            join_path("metros", "lines_metros.csv"),
        )

    def get_all_Bus_lines_json(self):
        df_disruptions, df_lines = self.factor_data("Bus")
        self.df_to_csv(
            df_disruptions,
            df_lines,
            join_path("bus", "disruptions_bus.csv"),
            join_path("bus", "lines_bus.csv"),
        )

    def get_all_Tramway_lines_json(self):
        df_disruptions, df_lines = self.factor_data("Tramway")
        self.df_to_csv(
            df_disruptions,
            df_lines,
            join_path("tramways", "disruptions_tram.csv"),
            join_path("tramways", "lines_tramways.csv"),
        )

    def get_all_LocalTrains_lines_json(self):
        df_disruptions, df_lines = self.factor_data("LocalTrain")
        self.df_to_csv(
            df_disruptions,
            df_lines,
            join_path("localtrains", "disruptions_localtrains.csv"),
            join_path("localtrains", "lines_localtrains.csv"),
        )

    def get_all_RapidTransit_lines_json(self):
        df_disruptions, df_lines = self.factor_data("RapidTransit")
        self.df_to_csv(
            df_disruptions,
            df_lines,
            join_path("rapidtransits", "disruptions_rapidtransit.csv"),
            join_path("rapidtransits", "lines_rapidtransits.csv"),
        )

    # Get all close points
    def get_all_pois_json(self, suffix="pois/"):
        uurl = self.url_base + suffix
        response = requests.get(uurl, headers=self.headers)

    def get_all_poi_types_json(self, suffix="poi_types/"):
        uurl = self.url_base + suffix
        response = requests.get(uurl, headers=self.headers)
