import pandas as pd

def merge_fruad_data(df1, df2):  # Accept DataFrames
    """Merges two DataFrames based on IP address ranges."""
    try:
        def ip_to_int(ip_address):
            try:
                parts = ip_address.split('.')
                return sum(int(part) * (256 ** i) for i, part in enumerate(reversed(parts)))
            except (AttributeError, ValueError):  # Handle potential errors
                return None

        df1['ip_int'] = df1['ip_address'].apply(ip_to_int)
        df2['lower_int'] = df2['lower_bound_ip_address'].apply(ip_to_int)
        df2['upper_int'] = df2['upper_bound_ip_address'].apply(ip_to_int)
        df2.dropna(inplace=True)

        merged_df = pd.merge_asof(
            df1.sort_values('ip_int'),
            df2[['lower_int', 'upper_int', 'country']].sort_values('lower_int'),
            left_on='ip_int',
            right_on='lower_int',
            direction='forward'
        )

        merged_df = merged_df[merged_df['ip_int'] <= merged_df['upper_int']]
        merged_df.drop(columns=['ip_int', 'lower_int', 'upper_int'], inplace=True)

        return merged_df

    except Exception as e:
        print(f"An error occurred during the merging process: {e}")
        return None  # Return None on error