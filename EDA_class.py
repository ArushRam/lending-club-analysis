import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

class EDA:
    def __init__(self, data):
        self.df = data

        # create a single fico metric as fico_range_high and fico_range_low are extremely correlated
        self.df['fico'] = (self.df['fico_range_high'] + self.df['fico_range_low'])/2
        # create cr_line_yrs for how long someone has had a credit line
        self.df['cr_line_yrs'] = (self.year_converter('issue_d') - self.year_converter('earliest_cr_line'))

    def year_converter(self, var):
        # convert dates from given format to a format that can be used arithmetically and in plots
        years = self.df[var].str[-4:].astype(np.float64)
        months = self.df[var].apply(lambda issue_d: dt.datetime.strptime(issue_d[:3], "%b").month)
        return years + ((1/12) * months)

    def default_rate_barplot(self, split, rotate=False):
        df = self.df
        buckets = sorted(df[split].unique())
        rates = []
        # compute default rate for each bucket (category within categorical variable)
        for bucket in buckets:
            total = len(df[df[split] == bucket])
            if total == 0:
                # division by zero error
                rates.append(0)
            else:
                rates.append(len(df[(df['loan_status'] == 'Charged Off') & (df[split] == bucket)])/total)
        plt.figure(figsize = (15, 8))
        plt.bar(x=buckets, height=rates)
        if rotate:
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

        # process years
        df['issue_year'] = self.year_converter('issue_d')
        years = sorted(df["issue_year"].unique())

        # compute rates
        int_rates = [df[df["issue_year"] == year]["int_rate"].mean() for year in years]
        def_rates = [len(df[(df["issue_year"] == year) & (df["loan_status"] == "Charged Off")])/len(df[df["issue_year"] == year]) * 100 for year in years]
        
        plt.plot(years, int_rates, label='Average Interest Rate')
        plt.plot(years, def_rates, label='Average Default Rate')
        plt.xlabel('Year')
        plt.ylabel('Rate (%)')
        plt.legend()
        print("Correlation: ", np.corrcoef(int_rates, def_rates)[0][1])

    def incomes_barplot(self, split):
        df = self.df
        plt.figure(figsize = (15, 8))
        buckets = df[split].unique()

        # compute mean incomes
        mean_incomes = [df[df[split] == bucket]['annual_inc'].mean() for bucket in buckets]

        plt.bar(x=buckets, height=mean_incomes)
        plt.xlabel(split)
        plt.ylabel("Average Income ($)")
        plt.xticks(rotation=90)
        return mean_incomes

    def boxplot(self, x, y, sort=False, hue=None):
        df = self.df
        plt.figure(figsize = (15, 8))
        if not sort:
            sns.boxplot(data=df, x=x, y=y, hue=hue)
        else:
            sns.boxplot(data=df, x=x, y=y, order=sorted(df[x].unique()), hue=hue)

    def correlation(self, x, y):
        print('Correlation: ', np.corrcoef(self.df[x], self.df[y])[0][1])





#yo = EDA_class(pd.read_csv('accepted_2007_to_2018Q4.csv'))

print(dt.datetime.strptime("Aug", "%b").month)