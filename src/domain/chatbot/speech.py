import math

from . import constants
from .regression_model import RegressionModel
from .text_classification import TextClassification
from .diet_generator import DietGenerator
from src.domain.entity.messageRS import MessageRS, MessageType


class Speech:
    LENGTH_FORM = len(constants.form) - 1
    form = constants.form

    def __init__(self):
        self.regression_model = RegressionModel()
        self.text_classification = TextClassification()
        self.diet_generator = DietGenerator()
        self.question_number = 0
        self.user_data = {}

    def out_coming_message(self, user_input, key, username):
        if key == 'start':
            self.__update_form_with_username(username)
            return self.__start()
        elif key == 'reply':
            return self.__reply(user_input)
        elif key == 'diet':
            return self.__diet()
        else:
            return self.__help()

    def __start(self):
        self.question_number = 2
        return MessageRS(self.form[0:self.question_number + 1], MessageType.TEXT)

    def __reply(self, user_input):
        self.__add_response_to_user_data(user_input)
        self.question_number += 1
        if self.question_number > self.LENGTH_FORM:
            return None

        if self.question_number < self.LENGTH_FORM:
            output = [self.form[self.question_number]]
        else:
            response = self.__get_response()
            output = [response, self.form[self.question_number]]

        return MessageRS(output, MessageType.TEXT)

    def __diet(self):
        return MessageRS([self.user_data["diet"]], MessageType.FILE)

    def __help(self):
        return MessageRS([constants.help], MessageType.TEXT)

    def __add_response_to_user_data(self, user_input):
        if self.question_number in [2, 3]:
            user_input = float(user_input.replace(',', '.'))

        column = constants.columns[self.question_number - 2]
        self.user_data[column] = user_input

    def __update_form_with_username(self, username):
        self.form[0] = self.form[0].format(username=username)
        self.form[6] = self.form[6].format(username=username)

    def __get_response(self):
        self.__get_allergies_and_diseases()

        objective = self.__get_objective()
        self.__get_diet(objective)
        self.user_data["objective"] = constants.objectives[objective].format(height=int(self.user_data["height"]))

        response = constants.final_response.format(objective=self.user_data["objective"],
                                                   allergies=self.user_data["allergy"],
                                                   diseases=self.user_data["disease"])
        return response

    def __get_allergies_and_diseases(self):
        user_input_data = [(self.user_data[key]) for key in ('allergy', 'disease')]
        allergies_and_diseases = self.text_classification.get_allergies_and_diseases_from_user_input(user_input_data)

        allergies, diseases = constants.format_allergies_and_diseases(allergies_and_diseases)

        for key, value in allergies_and_diseases.items():
            sentence = ''
            if value is not None:
                if key == 'allergy':
                    sentence = allergies.format(allergy=value)
                if key == 'disease':
                    sentence = diseases.format(disease=value)

            self.user_data[key] = sentence

    def __get_objective(self):
        user_input_data = [(self.user_data[key]) for key in ('height', 'weight')]
        return int(self.regression_model.predict(user_input_data))

    def __get_diet(self, objective):
        diet = self.diet_generator.build_diet(objective, self.user_data["allergy"])
        self.user_data["diet"] = diet
