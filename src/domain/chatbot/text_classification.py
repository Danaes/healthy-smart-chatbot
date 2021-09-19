import json
import unidecode

from spacy.lang.es import Spanish
from spacy.matcher import PhraseMatcher


class TextClassification:

    def __init__(self):
        with open('../../../resources/data/clear_data.json') as fp:
            self.data = json.load(fp)

        self.nlp = Spanish()
        self.matcher = self.__setup_matcher()

    def get_allergies_and_diseases_from_user_input(self, user_input):
        sentences = None
        for sentence in user_input:
            sentence = unidecode.unidecode(sentence).lower()

            if sentences is None:
                sentences = sentence
            else:
                sentences = ". ".join((sentences, sentence))

        doc = self.nlp(sentences)

        return self.__get_types(doc)

    def __setup_matcher(self):
        matcher = PhraseMatcher(self.nlp.vocab)
        allergy = list(self.nlp.pipe(self.data['allergy']))
        disease = list(self.nlp.pipe(self.data['disease']))
        matcher.add("allergy", None, *allergy)
        matcher.add("disease", None, *disease)

        return matcher

    def __get_types(self, doc):
        output = {'allergy': None, 'disease': None}
        for match_id, start, end in self.matcher(doc):
            key = doc.vocab.strings[match_id]
            word = str(doc[start:end])

            if output[key] is None:
                output[key] = word
            else:
                output[key] = ", ".join((output[key], word))

        return output
