import abc
import requests
from bs4 import BeautifulSoup

class TargetURIFactory:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def get_uri(self, key):
        pass

class Crawler:
    
    def __init__(self, target_series, uri_factory, parse_rule):
        self.target_series = target_series
        self.parse_rule = parse_rule
        self.uri_factory = uri_factory
    
    def find_all(self, selector, parser):
        self.crawl_result = {}
        for k in selector.keys():
            self.crawl_result[k] = []
            
        seq = 0
        for k, v in self.target_series.items():
            uri = self.uri_factory.get_uri(v)
            print(uri)
            try:
                response = requests.get(uri)
                soup = BeautifulSoup(response.content, parser)
                for k, s in selector.items():
                    selection = soup.select_one(s)
                    self.crawl_result[k].append(self.apply_parse_rule(k, selection))
                    print(seq, ")parsed - ", self.crawl_result[k][-1])
            except:
                for k, s in selector.items():
                    self.crawl_result[k].append("")
                    print(seq, ")parsed - failed")
            seq = seq + 1
            
        return self.crawl_result
    
    def apply_parse_rule(self, key, selection):
        if self.parse_rule is None or selection is None:
            return ""
        else:
            return self.parse_rule(key, selection)

                               
# class ColumnAdder:
    
#     def __init__(self, df, new_col_label, new_col_data):
#         self.df = df
#         self.new_col_label = new_col_label
#         self.new_col_data = new_col_data
    
#     def add():
#         self.df[new_col_label] = new_col_data
    
#     def save(csv_path):
#         self.df.to_csv(csv_path)
    
#     def add_and_save(csv_path):
#         self.add()
#         self.save(csv_path)
