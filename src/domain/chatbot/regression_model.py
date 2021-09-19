import pickle


class RegressionModel:
    def __init__(self):
        self.model = pickle.load(open("../../../models/pickle_model.pkl", 'rb'))

    def predict(self, data):
        return self.model.predict([data])[0]
