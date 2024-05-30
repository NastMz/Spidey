from api.config import model
from api.models import TopicWordModel, TopicDataModel, DataListModel


class TopicService:
    @staticmethod
    def get_topics():
        all_topics = model.get_topics()

        topics_data = [
            TopicDataModel(
                words=[
                    TopicWordModel(word=word, probability=prob).to_dict()
                    for word, prob in model.get_topic(topic)
                ],
                topic=str(topic)
            ).to_dict()
            for topic in all_topics
        ]

        data = DataListModel(
            data=topics_data
        )

        return data.to_dict()
