class SortGetTime(object):
    def __init__(self, data, date_column):
        self.data = data
        self.date_column = date_column

    def sort(self):
        self.data = self.data.sort_values(by=[self.date_column])
        self.data = self.data.reset_index()
        self.data = self.data.drop(columns="index")
        return self.data

    def get_time(self):
        first_day = self.data[self.date_column][0]
        last_day = self.data[self.date_column][len(self.data[self.date_column])-1]
        return (self.data, first_day, last_day)
