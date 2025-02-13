import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, chi2_contingency
from sklearn.preprocessing import  StandardScaler

def plot_histograms(data, num_cols, bins=10, figsize=(4, 2)):
     """
     Plots histograms for specified numerical columns in a DataFrame.
    """
     for col in num_cols:
       plt.figure(figsize=figsize)
       plt.hist(data[col], bins=bins)
       plt.xlabel(col)
       plt.ylabel('Frequency')
       plt.title(f'Histogram of {col}')
       plt.show()

def bivariate_analysis(df, var1, var2):
    """
    Performs bivariate analysis between two variables in a Pandas DataFrame.
    """

    if df[var1].dtype in ['int64', 'float64'] and df[var2].dtype in ['int64', 'float64']:  # Numerical vs. Numerical
        # Scatter plot
        plt.figure(figsize=(4, 2))
        sns.scatterplot(x=var1, y=var2, data=df)
        plt.title(f'Scatter Plot of {var1} vs. {var2}')
        plt.xlabel(var1)
        plt.ylabel(var2)
        plt.show()

        # Correlation coefficient
        correlation, p_value = pearsonr(df[var1], df[var2])
        print(f"Pearson Correlation Coefficient: {correlation:.2f}")
        print(f"P-value: {p_value:.3f}")

        # Regression line (optional)
        sns.regplot(x=var1, y=var2, data=df, scatter_kws={'s':20}, line_kws={'color':'red'}) #added regression line
        plt.show()

    elif df[var1].dtype in ['int64', 'float64'] and df[var2].dtype == 'object':  # Numerical vs. Categorical
        # Box plot or violin plot
        plt.figure(figsize=(4, 2))
        sns.boxplot(x=var2, y=var1, data=df)  # or sns.violinplot(...)
        plt.title(f'Box Plot of {var1} by {var2}')
        plt.xlabel(var2)
        plt.ylabel(var1)
        plt.show()

        # ANOVA (Analysis of Variance) -  Check for significant differences in means
        from scipy.stats import f_oneway
        groups = [df[var1][df[var2] == category] for category in df[var2].unique()]
        f_statistic, p_value = f_oneway(*groups)
        print(f"ANOVA F-statistic: {f_statistic:.2f}")
        print(f"P-value: {p_value:.3f}")

    elif df[var1].dtype == 'object' and df[var2].dtype == 'object':  # Categorical vs. Categorical
        # Cross-tabulation (contingency table)
        contingency_table = pd.crosstab(df[var1], df[var2])
        print("Contingency Table:\n", contingency_table)

        # Heatmap of contingency table
        plt.figure(figsize=(4, 2))
        sns.heatmap(contingency_table, annot=True, cmap="YlGnBu")  # Added Heatmap
        plt.title(f'Heatmap of {var1} vs. {var2}')
        plt.show()

        # Chi-squared test
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        print(f"Chi-squared statistic: {chi2:.2f}")
        print(f"P-value: {p:.3f}")

    else:
        print("Unsupported variable types for bivariate analysis.")

def standard_scaling(data):
    """
    Performs Standard scaling (Z-score normalization) on the input data.
    """
    scaler = StandardScaler()  # Create a StandardScaler object
    scaled_data = scaler.fit_transform(data) # Fit and transform the data
    return scaled_data

