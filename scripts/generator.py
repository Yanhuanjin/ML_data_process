import pandas as pd


class GenerateDate(object):

    def __init__(self, first_day, last_day):
        self.first_day = first_day
        self.last_day = last_day

    def generate(self, freq="D"):
        generated_date = pd.date_range(self.first_day, self.last_day, freq=freq)
        return generated_date