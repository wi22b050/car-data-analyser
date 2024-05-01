from analyze_data import AnalyseCarData
from io import BytesIO

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:
    def __init__(self, dataframe):
        self.df = dataframe
        self.analyzer = AnalyseCarData()
        self.buf = BytesIO()

    def plot_price_distribution(self):
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Model', y='Price', hue='year', data=self.df)
        plt.title('Price in EURO Distribution by Model and Year')
        plt.savefig(self.buf, format='png')
        plt.close()
        self.buf.seek(0)
        return self.buf.getvalue()


    def plot_average_price_comparison(self):
        plt.figure(figsize=(14, 8))
        ax = sns.barplot(x='Model', y='Price', hue='Source', data=self.df)
        plt.title('Average Price Comparison Across Datasets')
        plt.ylabel('Average Price')
        plt.xlabel('BMW Model')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.legend(title='Source')
        plt.tight_layout() 
        plt.savefig(self.buf, format='png')
        plt.close()
        self.buf.seek(0)
        return self.buf.getvalue()


    def plot_model_counts(self):
        company_model_counts = self.analyzer.count_bmw_company_models()
        web_model_counts = self.analyzer.count_bmw_web_models()

        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6), sharey=True)

        #company:
        sns.barplot(x='Model', y='Count', data=company_model_counts, ax=axes[0])
        axes[0].set_title('Model Counts in Company Data')
        axes[0].set_xlabel('BMW Model')
        axes[0].set_ylabel('Count')
        axes[0].tick_params(axis='x', rotation=45)

        #web:
        sns.barplot(x='Model', y='Count', data=web_model_counts, ax=axes[1])
        axes[1].set_title('Model Counts in Web Data')
        axes[1].set_xlabel('BMW Model')
        axes[1].tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.savefig(self.buf, format='png')
        plt.close()
        self.buf.seek(0)
        return self.buf.getvalue()


    def plot_price_difference_comparison(self):
        # Retrieve the price comparison data
        price_comparison_df = self.analyzer.compare_prices_across_datasets()
        # Create a visualization
        plt.figure(figsize=(14, 8))
        ax = sns.barplot(x='Model', y='Price_Difference', hue='Fuel', data=price_comparison_df)
        plt.title('Price Difference Comparison Across Datasets')
        plt.ylabel('Price Difference')
        plt.xlabel('BMW Model')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.legend(title='Fuel')
        plt.tight_layout()
        plt.savefig(self.buf, format='png')
        plt.close()
        self.buf.seek(0)
        return self.buf.getvalue()
    
