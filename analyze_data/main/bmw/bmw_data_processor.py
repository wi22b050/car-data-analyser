import pandas as pd
"""
Perpose -> Clean, prepare and merge data from both company CSV's!
"""
class BMWDataProcessor:
    def __init__(self, fahrzeugstamm_path, transaktion_path):
        self.fahrzeugstamm_path = fahrzeugstamm_path
        self.transaktion_path = transaktion_path
        self.merged_df = None
        self.cleaned_df = None

    def read_and_merge(self):
        fahrzeugstamm_df = pd.read_csv(self.fahrzeugstamm_path)
        transaktion_df = pd.read_csv(self.transaktion_path)
        fahrzeugstamm_df = fahrzeugstamm_df[['fahrzeug_id', 'marke', 'modell', 'ps', 'treibstoff']]
        transaktion_df = transaktion_df[['fahrzeug_id', 'preis', 'date']]
        self.merged_df = pd.merge(fahrzeugstamm_df, transaktion_df, on='fahrzeug_id')
        self.merged_df.rename(columns={'date': 'year'}, inplace=True)

    def drop_null_values(self):
        if self.merged_df is not None:
            self.merged_df = self.merged_df.dropna()
        else:
            print("Data not merged yet. Please run read_and_merge() first.")

    def drop_zero_values(self):
        if self.merged_df is not None:
            self.merged_df['year'] = pd.to_numeric(self.merged_df['year'], errors='coerce')
            self.merged_df = self.merged_df[
                (self.merged_df['ps'] != 0) &
                (self.merged_df['preis'] != 0) &
                (self.merged_df['treibstoff'] != '0') &
                (self.merged_df['year'] != 0)
            ].dropna(subset=['year'])
        else:
            print("Data not merged yet. Please run read_and_merge() first.")

    def additional_cleaning(self):
        # To clean year, convert it to a string, then to numeric and through that encounter "null"-values, if present:
        self.merged_df['year'] = self.merged_df['year'].astype(str)
        self.merged_df['year'] = pd.to_numeric(self.merged_df['year'], errors='coerce')
        self.merged_df.dropna(subset=['year'], inplace=True)
        # Ensure 'year' is an integer after dropping NaNs
        self.merged_df['year'] = self.merged_df['year'].astype(int)
        
        # Search for hybrids, if found, normalize them to Hybrid (without the additional information):
        self.merged_df['treibstoff'] = self.merged_df['treibstoff'].apply(lambda x: 'Hybrid' if 'Hybrid' in x else x)

        self.merged_df['modell'] = self.merged_df['modell'].replace({'3er': '3er-Reihe', '5er': '5er-Reihe'})
        
        self.merged_df['ps'] = self.merged_df['ps'].astype(int)

    def filter_bmw_models(self):
        if self.merged_df is not None:
            bmw_models = ['X1', 'X3', '3er-Reihe', '5er-Reihe']
            self.cleaned_df = self.merged_df[
                (self.merged_df['marke'] == 'BMW') & 
                (self.merged_df['modell'].isin(bmw_models))
            ]
        else:
            print("Data not cleaned yet!")

    def export_to_csv(self):
        output_path = 'analyze_data/cleaned_bmw_data.csv'
        if self.cleaned_df is not None:
            self.cleaned_df.to_csv(output_path, index=False)
            print(f"Data exported to CSV at: {output_path}")
        else:
            print("No data to export!")

            
# Please adjust your path! 
processor = BMWDataProcessor('analyze_data/Fahrzeugstamm.csv', 'analyze_data/Transaktion.csv')
# directories: Fahrzeugstamm: /Users/bonivircheva/Desktop/CarDataAnalyser/analyze_data/Fahrzeugstamm.csv, Transkationstamm: /Users/bonivircheva/Desktop/CarDataAnalyser/analyze_data/Transaktion.csv
# directory of bmw_data_processor: /Users/bonivircheva/Desktop/CarDataAnalyser/analyze_data/main/bmw/bmw_data_processor.py
processor.read_and_merge()
processor.drop_null_values()
processor.drop_zero_values()
processor.additional_cleaning()
processor.filter_bmw_models()
processor.export_to_csv()
