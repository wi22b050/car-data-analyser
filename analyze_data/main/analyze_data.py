import pandas as pd

class AnalyseCarData:
    def __init__(self):
        # Load and prepare the cleaned Company's dataset
        self.company_df = pd.read_csv('../cleaned_bmw_data.csv')
        self.company_df['year'] = pd.to_datetime(self.company_df['year'], format='%Y%m%d').dt.year
        self.company_df.rename(columns={'modell': 'Model', 'ps': 'PS', 'treibstoff': 'Fuel', 'preis': 'Price'}, inplace=True)
        self.company_df['Source'] = 'Company'

        # Load and prepare the cleaned Willhaben dataset
        self.web_df = pd.read_csv('../cleaned_bmw_data_web.csv')
        self.web_df['Year'] = pd.to_datetime(self.web_df['Year']).dt.year
        self.web_df['Price'] = pd.to_numeric(self.web_df['Price'], errors='coerce')
        self.web_df = self.web_df.dropna(subset=['Price'])
        self.web_df['Price'] = self.web_df['Price'].apply(int)
        self.web_df.rename(columns={'Year': 'year', 'Model': 'Model', 'PS': 'PS', 'Fuel': 'Fuel'}, inplace=True)
        self.web_df['Source'] = 'Web'

        self.common_years = set(self.company_df['year']).intersection(set(self.web_df['year']))
        self.common_models = set(self.company_df['Model']).intersection(set(self.web_df['Model']))
        self.common_ps = set(self.company_df['PS']).intersection(set(self.web_df['PS']))
        self.common_fuels = set(self.company_df['Fuel']).intersection(set(self.web_df['Fuel']))

        # Filter each dataset for rows where model, year, PS, and fuel are common
        self.company_df_filtered = self.company_df[
            (self.company_df['Model'].isin(self.common_models)) &
            (self.company_df['year'].isin(self.common_years)) &
            (self.company_df['PS'].isin(self.common_ps)) &
            (self.company_df['Fuel'].isin(self.common_fuels))
        ]

        self.web_df_filtered = self.web_df[
            (self.web_df['Model'].isin(self.common_models)) &
            (self.web_df['year'].isin(self.common_years)) &
            (self.web_df['PS'].isin(self.common_ps)) &
            (self.web_df['Fuel'].isin(self.common_fuels))
        ]

        self.combined_df = pd.concat([self.company_df_filtered, self.web_df_filtered], ignore_index=True)
        

    # 1) Whats the price difference for the same models with the same year, fuel and ps across all datasets? 
    def compare_prices_across_datasets(self) -> dict:
        # Group and calculate mean prices
        grouped_prices = self.combined_df.groupby(['Model', 'year', 'PS', 'Fuel', 'Source'])['Price'].mean().reset_index()

        # Pivot the table to compare prices
        pivot_prices = grouped_prices.pivot_table(values='Price', index=['Model', 'year', 'PS', 'Fuel'], columns='Source', fill_value=0).reset_index()

        # Calculate the price difference and round to 2 decimals
        pivot_prices['Price_Difference'] = (pivot_prices['Company'] - pivot_prices['Web']).round(2)

        # Exclude rows where the Web price is 0
        pivot_prices = pivot_prices[(pivot_prices['Web'] != 0) & (pivot_prices['Company'] != 0)]
        return pivot_prices
    
    # 2) What's the average price of the different bmw models, based on year, ps, and fuel?
    def analyse_company_models(self) -> dict:
        # Filter out prices below 15000 and calculate the average price per group
        filtered_company = self.company_df[self.company_df['Price'] > 15000]
        avg_prices_company = filtered_company.groupby(['Model', 'year', 'PS', 'Fuel'])['Price'].mean().reset_index()
        return avg_prices_company

    def analyse_web_models(self) -> dict:
        # Filter out prices below 15000 and calculate the average price per group
        filtered_web = self.web_df[self.web_df['Price'] > 15000]
        avg_prices_web = filtered_web.groupby(['Model', 'year', 'PS', 'Fuel'])['Price'].mean().reset_index()
        return avg_prices_web
    
    # 3) How many models were collected across the datasets?
    def count_bmw_company_models(self) -> dict:
        model_counts_company = self.company_df.groupby('Model').size().reset_index(name='Count')
        return model_counts_company

    def count_bmw_web_models(self) -> dict:
        model_counts_web = self.web_df.groupby('Model').size().reset_index(name='Count')
        return model_counts_web
    
    
