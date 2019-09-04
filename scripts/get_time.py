class GetTime(object):
    def __init__(self, data, date_column):
        self.data = data
        self.date_column = date_column

    def get_time(self):
        first_day = self.data[self.date_column][0]
        last_day = self.data[self.date_column][len(self.data[self.date_column]) - 1]
        return (self.data, first_day, last_day)
