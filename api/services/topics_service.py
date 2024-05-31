import pandas as pd

from api.config import model
from api.models import TopicWordModel, TopicDataModel, DataListModel, PredictedTopicModel, IntertopicDistance


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

    @staticmethod
    def get_topic(topic_id):
        topic_words = [
            TopicWordModel(word=word, probability=prob).to_dict()
            for word, prob in model.get_topic(topic_id)
        ]

        topic_data = TopicDataModel(
            words=topic_words,
            topic=str(topic_id)
        )

        return topic_data.to_dict()

    @staticmethod
    def predict_topic(text):
        topic, prob = model.transform(text)

        data = PredictedTopicModel(
            topic=str(topic[0]),
            probability=float(prob[0])
        )

        return data.to_dict()

    @staticmethod
    def get_vizualization_data():
        df = pd.read_csv('topic_visualization_data.csv')

        vizualization_data = [
            IntertopicDistance(
                coordinates=[item['x'], item['y']],
                topic=item['Topic'],
                words=item['Words'],
                size=item['Size']
            ).to_dic()
            for item in df
        ]
        
        data = DataListModel(
            data=vizualization_data
        )

        return data.to_dict()