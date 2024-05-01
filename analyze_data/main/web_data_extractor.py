from bmw.pages import Pages 
from utilities.helpers import Cleaner
import re

import pandas as pd


"""
Perpose -> Extract, clean and prepare data from willhaben.at!
"""
class CarDataExtractor:
    def __init__(self):
        self.valid_years = ['2020', '2021', '2022', '2023']

    def extract_data(self, html_string, model):
        # Initialize lists for data collection
        gather_prices = []
        gather_ps = []
        gather_years = []
        gather_fuel = []
        # Create patterns, to search through the html-document:
        pattern_prices = "search-result-entry-price-.{100}"
        pattern_ps = 'Text-sc-10o2fdq-0 gjhjpn"><span class="Text-sc-10o2fdq-0.{15}'
        pattern_year = 'class="Text-sc-10o2fdq-0 dZlWCx"><span class="Text-sc-10o2fdq-0 gTqzpY.{10}'
        pattern_fuel = 'Text-sc-10o2fdq-0 bFMMYK.{70}'

        # Find all matches in the string
        matches_prices = re.findall(pattern_prices, html_string)
        matches_ps = re.findall(pattern_ps, html_string)
        matches_year = re.findall(pattern_year, html_string)
        matches_fuel = re.findall(pattern_fuel, html_string)

        # Add the found data to the data collection lists:
        for match in matches_prices:
            gather_prices.append(match)

        for match in matches_ps:
            gather_ps.append(match)

        for match in matches_year:
            gather_years.append(match)

        for match in matches_fuel:
            gather_fuel.append(match)

        # Strip parts of the data we dont need:
        part_to_strip_ps = 'Text-sc-10o2fdq-0 gjhjpn"><span class="Text-sc-10o2fdq-0'
        part_to_strip_year = 'class="Text-sc-10o2fdq-0 dZlWCx"><span class="Text-sc-10o2fdq-0 gTqzpY'
        part_to_strip_fuel = "Text-sc-10o2fdq-0 bFMMYK"

        # Strip the part from each element of the list
        stripped_list = [element.replace(part_to_strip_ps, "") for element in gather_ps]
        stripped_list_years = [element.replace(part_to_strip_year, "") for element in gather_years]
        stripped_list_fuel = [element.replace(part_to_strip_fuel, "") for element in gather_fuel]


        filtered_fuel_list = []
        for item in stripped_list_fuel:
            # Split the string by comma and take the first element, which is the fuel type:
            fuel_type = item.split(",")[0].replace('">', '').strip()
            filtered_fuel_list.append(fuel_type)

        page1_ps = [re.search(r'\d+', s).group() for s in stripped_list]
        page1_years_strip = [re.search(r'\d+', s).group() for s in stripped_list_years]

        # Further strip the valid years
        valid_years = ['2020', '2021', '2022', '2023']
        filtered_years = [year for year in page1_years_strip if year in valid_years]
        

        # Create a regex based on the "€"-symbol, create a matcher and extend the prices list with the found matches:
        price_pattern = re.compile(r'€\s*\d+[\.,]?\d*')
        extracted_prices = []
        for string in gather_prices:
            matches = price_pattern.findall(string.replace(".", ""))
            extracted_prices.extend(matches)

        # Calculate the maximum length of the data lists(important for the dataframe creation! ):
        max_length = max(len(extracted_prices), len(filtered_years), len(page1_ps), len(filtered_fuel_list))

        # Pad the lists with 'NA' to make sure they all have the same length:
        extracted_prices += ['NA'] * (max_length - len(extracted_prices))
        filtered_years += ['NA'] * (max_length - len(filtered_years))
        page1_ps += ['NA'] * (max_length - len(page1_ps))
        filtered_fuel_list += ['NA'] * (max_length - len(filtered_fuel_list))

        # Create a DataFrame
        data = {
            'Brand': ['BMW'] * max_length,
            'Model': [model] * max_length,
            'Price': extracted_prices,
            'Year': filtered_years,
            'PS': page1_ps,
            'Fuel': filtered_fuel_list
        }

        df = pd.DataFrame(data)
        return df


    def process_pages(self, pages_dict):
        # Initialize large lists to aggregate data from all pages:
        all_prices = []
        all_years = []
        all_ps = []
        all_fuels = []
        all_brands = []
        all_models = []
        # Determine the correct model name based on the key used in pages_dict
        for model_key, page_list in pages_dict.items():
            if model_key == '3er-Reihe':
                model_name = '3er-Reihe'
            elif model_key == '5er-Reihe':
                model_name = '5er-Reihe'
            elif model_key == 'X1':
                model_name = 'X1'
            elif model_key == 'X3':
                model_name = 'X3'
            else:
                model_name = 'Unknown'

            for page_html in page_list:
                # Extract data for a single page:
                df = self.extract_data(page_html, model_name)
                
                # Extend lists with the aggragated data from multiple pages:
                all_prices.extend(df['Price'].tolist())
                all_years.extend(df['Year'].tolist())
                all_ps.extend(df['PS'].tolist())
                all_fuels.extend(df['Fuel'].tolist())
                all_brands.extend(['BMW'] * len(df))  
                all_models.extend([model_name] * len(df))  

        # Create the dataframe:
        combined_data = {
            'Brand': all_brands,
            'Model': all_models,
            'Price': all_prices,
            'Year': all_years,
            'PS': all_ps,
            'Fuel': all_fuels
        }
        combined_df = pd.DataFrame(combined_data)

        return combined_df



pages_instance = Pages()
pages_dict = {
    '3er-Reihe': pages_instance.returnPages_bmw_3(),
    '5er-Reihe': pages_instance.returnPages_bmw_fuenfer_reihe(),
    'X1': pages_instance.returnPages_bmw_x_eins(),
    'X3': pages_instance.returnPages_bmw_x_drei()
}

# Extract data
extractor = CarDataExtractor()
combined_df = extractor.process_pages(pages_dict)
# Clean data
cleaner = Cleaner(combined_df)
cleaner.clean_fuel()
cleaner.clean_prices()
cleaner.convert_years_pd_object()
cleaner.check_for_null_values()

# Please adjust your paths! 
# Export the cleaned DataFrame to a CSV file
csv_file_path = 'analyze_data/cleaned_bmw_data_web.csv'
combined_df.to_csv(csv_file_path, index=False)


