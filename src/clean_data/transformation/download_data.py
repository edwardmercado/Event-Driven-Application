# import requests, os
# from urllib.request import urlretrieve

linkUS = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
linkJH = "https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

dst1 = 'tmp/data_us.csv'
dst2 = 'tmp/data_john_hopkins.csv'

def downloadData():
    urlretrieve(linkUS, dst1)
    urlretrieve(linkJH, dst2)   