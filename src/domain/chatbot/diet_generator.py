import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import re


class DietGenerator:
    targets = ['hiper', 'normal', 'hipo']

    def __init__(self):
        self.base_path = '../../../resources/template'
        self.food = pd.read_csv('../../../resources/data/diets.csv', delimiter=';')

        env = Environment(loader=FileSystemLoader(self.base_path))
        self.template = env.get_template('diet.html')

    def build_diet(self, objective, allergies=None):
        objective = 2 if objective == 3 else objective
        target = self.targets[objective]

        food = self.food[self.food['Target'] == target].iloc[:, :-1]
        food = self.__remove_allergies(food['Food'], allergies)

        diet = self.__build_table(food)

        return self.__build_pdf(diet, target)

    def __remove_allergies(self, food, allergies):
        food_without_allergies = [None] * len(food)
        for idx_food, eats in enumerate(food):
            meals = [None] * len(eats.split('.'))
            for idx_meal, meal in enumerate(eats.split('.')):
                for allergy in allergies:
                    if allergy.lower() in meal.lower():
                        meal = re.sub(f'(?i){allergy}', '', meal)

                    meals[idx_meal] = meal

            food_without_allergies[idx_food] = '.'.join([str(meal) for meal in meals])

        food['Comida'] = food_without_allergies
        return food

    def __build_table(self, food):
        diet = food.rename(columns={'Day': 'Dia', 'Time': 'Hora', 'Food': 'Comida'})

        diet['Dia'] = pd.Categorical(diet['Dia'], ordered=True, categories=['Lunes', 'Martes', 'Miercoles', 'Jueves',
                                                                            'Viernes', 'Sabado', 'Domingo'])

        diet['Hora'] = pd.Categorical(diet['Hora'], ordered=True, categories=['Desayuno', 'Almuerzo', 'Comida',
                                                                              'Merienda', 'Cena'])

        diet = pd.pivot_table(diet, index=['Dia', 'Hora'], values='Comida', aggfunc='last')

        return diet

    def __build_pdf(self, diet, target):
        template_vars = {"title": "DIETA SEMANAL", "meal": diet.to_html()}
        html_out = self.template.render(template_vars)

        path_output_file = f'{self.base_path}/{target}.pdf'
        HTML(string=html_out).write_pdf(path_output_file)

        return path_output_file
