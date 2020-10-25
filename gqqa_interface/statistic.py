import pandas
import os
from base import BaseKnowledge

class GQQAHistory:

    def __init__(self, file):
        self.row = self._init_data()
        self.csv_file = file
        if not os.path.exists(file):
            self.df = pandas.DataFrame(self.row)
        else:
            self.df = pandas.read_csv(file, index_col=[0])

    def _init_data(self):
        return {
            'Paragraph': [],
            'Extracted Answer': [], 'Generated Question': [], 'Generated Answer': []
        }

    def add_qa_result(self, bkd: BaseKnowledge):
        for passage in bkd.passages:
            print(len(passage.aqset))
            for answer, _ in passage.aqset:
                self.row['Generated Answer'].append(answer)
        self.df = pandas.concat([self.df, pandas.DataFrame(self.row)])

    def add_qg_result(self, bkd: BaseKnowledge):
        for passage in bkd.passages:
            for answer, question in passage.aqset:
                self.row['Paragraph'].append(passage.text)
                self.row['Extracted Answer'].append(answer)
                self.row['Generated Question'].append(question)

    def to_html(self):
        return self.df.to_html()

    def save_csv(self):
        if not os.path.exists(self.csv_file):
            self.df.to_csv(self.csv_file, mode='w', index=True)
        else:
            self.df.to_csv(self.csv_file, mode='a', header=False, index=True)
        return self.df

    def clear(self):
        os.remove(self.csv_file)
        self.row = self._init_data()
        self.df = pandas.DataFrame(self.row)
