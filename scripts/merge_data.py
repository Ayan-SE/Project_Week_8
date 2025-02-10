import pandas as pd

def merge_data(file1, file2, file3, output_file, merge_on=None, how='inner'):
    """
    Merges three datasets (CSV or other Pandas-readable formats) into one.
    """

    try:
        df1 = pd.read_csv(file1)  # Or pd.read_excel(), pd.read_json(), etc.
        df2 = pd.read_csv(file2)
        df3 = pd.read_csv(file3)

        # First merge df1 and df2
        if merge_on:
           merged_df1_2 = pd.merge(df1, df2, on=merge_on, how=how)
        else:
           merged_df1_2 = pd.merge(df1, df2, how=how) #Pandas will try to find common columns


        # Then merge the result with df3
        if merge_on:
           final_merged_df = pd.merge(merged_df1_2, df3, on=merge_on, how=how)
        else:
           final_merged_df = pd.merge(merged_df1_2, df3, how=how)

        final_merged_df.to_csv(output_file, index=False)  # Save to CSV
        return final_merged_df

    except FileNotFoundError:
        print(f"Error: One or more input files not found.")
        return None
    except pd.errors.ParserError:  # Catch potential parsing errors
        print(f"Error: Could not parse one or more input files. Check the file format.")
        return None
    except KeyError:
        print(f"Error: Merge column(s) '{merge_on}' not found in one or more dataframes.")
        return None
    except Exception as e: # Catch any other potential errors
        print(f"An unexpected error occurred: {e}")
        return None