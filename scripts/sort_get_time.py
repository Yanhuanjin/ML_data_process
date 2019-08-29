class SortGetTime(object):
    def __init__(self, data):
        self.data = data

    def sort(self):
        self.data = self.data.sort_values(by=["DATE"])
        self.data = self.data.reset_index()
        self.data = self.data.drop(columns="index")
        return self.data

    def get_time(self):
        first_day = self.data["DATE"][0]
        last_day = self.data["DATE"][len(self.data["DATE"])-1]
        return (self.data, first_day, last_day)
