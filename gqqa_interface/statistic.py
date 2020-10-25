import pandas
from base import BaseKnowledge

class GQQAHistory:

    def __init__(self):
        self.clear()

    def clear(self):
        self.history = self._init_data()

    def _init_data(self):
        return {
            'Paragraph': [],
            'Extracted Answer': [], 'Generated Question': [], 'Generated Answer': []
        }

    def add_qa_result(self, bkd: BaseKnowledge):
        for passage in bkd.passages:
            print(len(passage.aqset))
            for answer, _ in passage.aqset:
                self.history['Generated Answer'].append(answer)

    def add_qg_result(self, bkd: BaseKnowledge):
        for passage in bkd.passages:
            for answer, question in passage.aqset:
                self.history['Paragraph'].append(passage.text)
                self.history['Extracted Answer'].append(answer)
                self.history['Generated Question'].append(question)

    def to_dataframe(self):
        return pandas.DataFrame(self.history)

    def to_html(self):
        return self.to_dataframe().to_html()