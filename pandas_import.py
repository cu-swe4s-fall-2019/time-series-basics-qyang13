import numpy as np
import pandas as pd
import datetime as dt
import argparse as ap
import os


def df_merge(df, csv):
    '''
    Merge dataframes based on rownames
    '''
    # Find the indix of cgm
    for i in range(len(csv)):
        if 'cgm' in csv[i]:
            idx = i

    temp = df.copy()
    del temp[idx]
    df_out = df[idx].join(temp, rsuffix='_'+str(i), how='left')
    return df_out


def df_format(df, csv):
    '''
    Format dataframes by:
        1. remove non-numeric values
        2. convert numeric values to float
        3. rename value column with corresponding file name
    '''
    for i in range(len(df)):
        col_names = str(csv[i].replace('_small.csv', ''))
        # Remove all rows with non-numeric value
        df[i] = df[i][pd.to_numeric(
            df[i]['value'], errors='coerce').notnull()]
        # Change all values to type float
        df[i]['value'] = df[i]['value'].astype(float)
        # rename the value to file name
        df[i].rename(columns={'value': col_names}, inplace=True)
    return df


def import_files(path, csv):
    '''
    Import files into dataframe, use time as the row name
    '''
    df = []
    for f in csv:
        df.append(pd.read_csv(path+f,
                  parse_dates=['time'], index_col=['time']))
    return df


def argparser():
    '''
    Argument Parser
    '''
    parser = ap.ArgumentParser(description='Time Series Input')
    parser.add_argument('--data_dir',
                        type=str,
                        help='Diretctory containing files to combine',
                        default='./smallData/')
    args = parser.parse_args()
    return args


def main():
    args = argparser()
    dir = args.data_dir
    csv = [f for f in os.listdir(dir) if os.path.isfile(dir+f)]
    df = import_files(dir, csv)
    # Step 2: Import the data and change value columns
    df = df_format(df, csv)
    # Step 3: Join the dataframes
    df_merged = df_merge(df, csv)
    # Step 4: replace NAN with 0
    df_merged = df_merged.fillna(0)
    # Step 5: round time
    df_merged.insert(len(df_merged.columns),
                     'time5', df_merged.index.round('5min'))
    df_merged.insert(len(df_merged.columns),
                     'time15', df_merged.index.round('15min'))
    # Step 6: Calculate mean or sum and merge the dataframes
    df_sum = df_merged[['activity', 'bolus', 'meal', 'time5', 'time15']]
    df_mean = df_merged[['smbg', 'hr', 'cgm', 'basal', 'time5', 'time15']]
    sum_5min = df_sum.groupby(['time5']).sum()
    mean_5min = df_mean.groupby(['time5']).mean()
    sum_15min = df_sum.groupby(['time15']).sum()
    mean_15min = df_mean.groupby(['time15']).mean()
    df_5min = sum_5min.join(mean_5min)
    df_15min = sum_15min.join(mean_15min)
    # Step 7: Write them to new csv files
    df_5min.to_csv('5min_small.csv', index=True, header=True)
    df_15min.to_csv('15min_small.csv', index=True, header=True)


if __name__ == '__main__':
    main()
