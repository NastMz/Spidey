import json

from api.models import BagOfWordsModel


class BagOfWordsService:
    @staticmethod
    def get_words():
        with open('bag_of_words.json', 'r') as file:
            data = json.load(file)

        bag = BagOfWordsModel(
            words=data
        )

        return bag.to_dict()
