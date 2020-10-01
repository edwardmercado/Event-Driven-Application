import os, glob
import pandas

def combineData():
    #combine data by date
    df1 = pandas.read_csv('tmp/data_john_hopkins.csv')
    df2 = pandas.read_csv('tmp/data_us.csv')

    df = df1.merge(df2, on='date')
    df.to_csv('tmp/combined/data_combined.csv', sep=',', index=False)

    #filter to unique dates
    df = pandas.read_csv('tmp/combined/data_combined.csv')
    df = df.drop_duplicates(subset='date', keep="last")
    df_reorder = df[['date', 'cases', 'recovered', 'deaths']] #reoder columns
    df_reorder.to_csv('tmp/combined/data_combined.csv', sep=',', index=False)

