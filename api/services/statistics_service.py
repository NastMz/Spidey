import json

import pandas as pd

from api.models import BarDataModel, DataListModel, PieDataModel, MapDataModel, TreeMapDataModel


class StatisticsService:
    @staticmethod
    def get_bar_data():
        df = pd.read_csv('universities_data.csv')

        records_per_university = df['university'].value_counts().sort_values(ascending=False)

        universities = records_per_university.index.tolist()
        records = records_per_university.values.tolist()

        bar_data = BarDataModel(
            categories=universities,
            data=records
        )

        return bar_data.to_dict()

    @staticmethod
    def get_pie_data():
        df = pd.read_csv('universities_data.csv')

        universities_per_country = df.groupby('country')['university'].nunique()

        pie_data = [
            PieDataModel(
                value=int(row),
                name=str(index)
            )
            for index, row in universities_per_country.items()
        ]

        pie_data_dicts = [data.to_dict() for data in pie_data]

        data = DataListModel(
            data=pie_data_dicts
        )

        return data.to_dict()

    @staticmethod
    def get_map_data():
        df = pd.read_csv('universities_data.csv')
        records_per_country = df['country'].value_counts().to_dict()

        with open('countries_coordinates.json', 'r') as file:
            coordinates_list = json.load(file)

        coordinates_dict = {entry['country']: entry['coords'] for entry in coordinates_list}

        map_data = [
            MapDataModel(
                country=country,
                coords=coordinates_dict[country],
                count=records_per_country.get(country, 0)
            )
            for country in records_per_country if country in coordinates_dict
        ]

        map_data_dicts = [data.to_dict() for data in map_data]

        data = DataListModel(
            data=map_data_dicts
        )

        return data.to_dict()

    @staticmethod
    def get_treemap_data():
        with open('bag_of_words.json', 'r') as file:
            bag_of_words = json.load(file)

        treemap_data = [
            TreeMapDataModel(
                name=word,
                value=count,
            )
            for word, count in bag_of_words.items()
        ]

        treemap_data_dicts = [data.to_dict() for data in treemap_data]

        total_count = sum(bag_of_words.values())

        data = DataListModel(
            data=[dict(
                name='Bag Of Words',
                value=total_count,
                children=treemap_data_dicts
            )]
        )

        return data.to_dict()
