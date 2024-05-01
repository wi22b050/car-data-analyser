import pandas as pd
import numpy as np

class Cleaner:

    def __init__(self, dataframe):
        self.dataframe = dataframe


    def clean_fuel(self):
        # If Hybrid is contained in any row, convert it to only hybrid.
        self.dataframe['Fuel'] = self.dataframe['Fuel'].apply(lambda x: 'Hybrid' if 'Hybrid' in x else x)


    def clean_prices(self):
        # Strip the "€"-Symbol and ",".
        self.dataframe['Price'] = self.dataframe['Price'].str.replace('€', '').str.replace(',', '').str.strip()


    def convert_years_pd_object(self):
        # Replace 'NA' with null value(numpy):
        self.dataframe['Year'] = self.dataframe['Year'].replace('NA', np.nan)
        # Convert year to pandas datetime object, errors='coerce' (handle remaining formats, if such are present!)
        self.dataframe['Year'] = pd.to_datetime(self.dataframe['Year'], format='%Y', errors='coerce')

    def check_for_null_values(self):
        # Checker function
        initial_null_values = self.dataframe.isnull().sum()
        print("Initial null values in each column:\n", initial_null_values)
        total_initial_nulls = initial_null_values.sum()
        print("Total initial null values in DataFrame:", total_initial_nulls)
        self.dataframe.dropna(inplace=True)
