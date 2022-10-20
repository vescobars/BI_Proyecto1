from pydantic import BaseModel

from DataModel import DataModel


class TestModel(BaseModel):
    def predict(self, data: str):
        if len(data) < 10:
            return {
                "response": "suicide",
                "original_input": data
            }
        else:
            return {
                "response": "nosuicide",
                "original_input": data
            }


class PredictionModel:
    model: TestModel

    def __init__(self):
        self.model = TestModel()

    def make_predictions(self, data: DataModel):
        result = self.model.predict(data.text)
        return result


