import pandas as pd

def filerData():
    df = pd.read_csv('tmp/data_john_hopkins.csv')
    df = df [['Date' ,'Recovered', 'Country/Region']]

    #filter to country = 'canada'
    select_US = df[df['Country/Region'] == 'US']
    select_US.to_csv('tmp/data_john_hopkins.csv', sep=',', index=False)

    #removed country
    df = df [['Date' ,'Recovered']]
    df.to_csv('tmp/data_john_hopkins.csv', sep=',', index=False)

    #modified header
    df = pd.read_csv('tmp/data_john_hopkins.csv', header=0, names=['date', 'recovered'], parse_dates=['date'])
    df.to_csv('tmp/data_john_hopkins.csv', sep=',', index=False)