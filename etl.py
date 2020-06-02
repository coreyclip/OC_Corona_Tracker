import csv
import os


class DataHandler:
    def __init__(self, path='./oc_overall_stats.csv', city_data_path='./oc_city_data.csv'):

        if os.path.isfile(path) and os.access(path, os.R_OK):
            with open(path) as file:
                reader = csv.reader(file)
                self.data = [row for row in reader]
        else:
            self.data = []
        if os.path.isfile(city_data_path) and os.access(city_data_path, os.R_OK):
            with open(city_data_path) as file:
                reader = csv.reader(file)
                self.city_data = [row for row in reader]
        else:
            self.city_data = []

        self.main_data_path = path
        self.city_data_path = city_data_path

    def append_data(self, new_data):

        if 'city' not in new_data.keys():
            self.data.append(new_data)
        else:
            self.city_data.append(new_data)


    def save_data(self):

        with open(self.main_data_path, 'w') as file:
            header = self.data[0].keys()
            w = csv.DictWriter(file, header)
            w.writeheader()
            for row in self.data:
                w.writerow(row)
        with open(self.city_data_path, 'w') as file:
            city_header = self.city_data[0].keys()
            w = csv.DictWriter(file, city_header)
            w.writeheader()
            for row in self.city_data:
                w.writerow(row)

