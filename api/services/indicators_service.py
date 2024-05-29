import json

from api.models import IndicatorsModel


class IndicatorsService:
    @staticmethod
    def get_indicators():
        with open('metadata.json', 'r') as file:
            data = json.load(file)

        indicators = IndicatorsModel(
            universities=data['num_universities'],
            countries=data['num_countries'],
            docs=data['num_records']
        )

        return indicators.to_dict()

