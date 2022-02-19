import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class EDA:
    def __init__(self, data=None):
        self.df = data

    def default_rate_barplot(self, split):
        df = self.df
        buckets = df[split].unique()
        rates = [len(df[(df['loan_status'] == 'Charged Off') & (df[split] == cat)])/len(df[df[split] == cat]) for cat in buckets]
        plt.figure(figsize = (15, 8))
        plt.bar(x=buckets, height=rates)
        plt.xticks(rotation = 90)
        plt.xlabel(split)
        plt.ylabel('Default Rate')
        return rates

    def loan_amount_barplot(self, split):
        plt.figure(figsize = (15, 8))
        ax = sns.boxplot(x=split, y='loan_amnt', data = self.df, hue='loan_status')
        ax.set_xlabel(split)
        ax.set_ylabel("Loan Amount ($)")
        ax.set_xticklabels(ax.get_xticklabels(),rotation = 90)

    def default_rate_by_purpose(self, purpose, split):
        df = self.df
        rates = []
        for item in df[split].unique():
            total = len(df[(df[split] == item) & (df['purpose'] == purpose)])
            if total == 0:
                rates.append(0)
            else:
                rates.append(len(df[(df['loan_status'] == 'Charged Off') & (df['purpose'] == purpose) & (df[split] == item)])/total)
        plt.figure(figsize = (15, 8))
        plt.bar(x=df[split].unique(), height=rates)
        plt.xticks(rotation = 90)
        plt.xlabel(split)
        plt.ylabel('Default Rate')

    def rates_by_year(self):
        df = self.df
        df['issue_year'] = df['issue_d'].str[-4:].astype(int)
        years = sorted(df["issue_year"].unique())
        irs = [df[df["issue_year"] == year]["int_rate"].mean() for year in years]
        drs = [len(df[(df["issue_year"] == year) & (df["loan_status"] == "Charged Off")])/len(df[df["issue_year"] == year]) * 100 for year in years]
        plt.plot(years, irs, label='Average Interest Rate')
        plt.plot(years, drs, label='Average Default Rate')
        plt.xlabel('Year')
        plt.ylabel('Rate (%)')
        print("Correlation: ", np.corrcoef(irs,drs)[0][1])

    def incomes_barplot(self, split):
        df = self.df
        plt.figure(figsize = (15, 8))
        buckets = df[split].unique()
        mean_incomes = [df[df[split] == bucket]['annual_inc'].mean() for bucket in buckets]
        plt.bar(x=buckets, height=mean_incomes)
        plt.xlabel(split)
        plt.ylabel("Average Income ($)")
        plt.xticks(rotation=90)
        return mean_incomes



#yo = EDA_class(pd.read_csv('accepted_2007_to_2018Q4.csv'))