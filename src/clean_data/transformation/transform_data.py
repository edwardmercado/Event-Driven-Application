import pandas as pd
import boto3, os, json, csv
from boto3.dynamodb.conditions import Key, Attr
from datetime import date

class Main:

    def __init__(self, url1, url2, dynamoDBTableName, snsTopicName):
        self.url1 = url1
        self.url2 = url2
        self.dynamoDBTableName = dynamoDBTableName
        self.today = date.today()
        self.counter = 0
        self.snsTopicName = snsTopicName
        self.notificationMessage = ""
        self.recoveredPerDay = 0
        self.casesPerDay = 0
        self.deathsPerDay = 0

    def readData(self):
        try:
            firstDF = pd.read_csv(self.url1)
            secondDF = pd.read_csv(self.url2)
            self.filterData(firstDF, secondDF)
        except Exception as e:
            self.notificationMessage = "Raw data's cannot be downloaded. ETL Job has failed. Reason: " + str(e)
            self.sendNotification()
            exit(1)

    def filterData(self, firstDF, secondDF):
        try:
            secondDF = secondDF.drop(["Deaths", "Confirmed"], axis=1) #drop NA columns
            combineDF = pd.merge(secondDF, firstDF, left_on='Date', right_on='date', how='outer')
            combineDF.columns = [column.replace("/", "_") for column in combineDF.columns]
            cleanDF = combineDF[combineDF.Country_Region=="US"]
            cleanDF = cleanDF.drop(["Province_State", "Lat", "Long", "date"], axis=1)
            #print(cleanDF.head(20))

            cleanDF = cleanDF.fillna(0)

            #convert float to int
            cleanDF['Recovered'] = cleanDF['Recovered'].astype(int)
            cleanDF['cases'] = cleanDF['cases'].astype(int)
            cleanDF['deaths'] = cleanDF['deaths'].astype(int)

            #print(cleanDF.tail(1))

            #drop data that has no date
            #cleanDF.dropna(subset=['Date'])
            self.saveData(cleanDF)

        except Exception as e:
            self.notificationMessage = "Raw data's cannot be filter. ETL Job has failed. Reason: " + str(e)
            self.sendNotification()
            exit(1)
        finally:
            #drop data that has no date
            cleanDF.dropna(subset=['Date'])
        

    def saveData(self, cleanDF):
        lastDateinDF = cleanDF.tail(1)
        lastDatetoJSON = lastDateinDF.T.to_dict().values()
        json_data = cleanDF.T.to_dict().values() #convert dataframe to json then store

        # print(lastDatetoJSON)
        # print(json_data)
        self.loadData(json_data, lastDatetoJSON)

    def loadData(self, jsonData, lastDateJSON):
        
        dynamodb = boto3.resource('dynamodb')
        tableName = dynamodb.Table(self.dynamoDBTableName)

        #Scan Table
        scanResp = tableName.scan(
            Limit = 10,
            Select = 'COUNT'
        )

        scanCount = scanResp['ScannedCount']

        # print("Scan Count: " + str(scanCount))
        # print(jsonData)

        # currentDay = self.today.strftime("%Y-%m-%d")
        # print("Current Day: " + str(currentDay))

        if scanCount == 0:
            self.initialUpdate(jsonData, tableName)
        else:
            self.dailyUpdate(lastDateJSON, tableName)

            
    def initialUpdate(self, jsonData, tableName):
        for entry in jsonData:
            self.counter+=1

            tableName.put_item(Item={
            'Date': entry["Date"],
            'Country_Region': entry["Country_Region"],
            'Recovered': entry["Recovered"],
            'cases': entry["cases"],
            'deaths': entry["deaths"]
        })
        self.notificationMessage = "ETL Job has completed. Updated " + str(self.counter) + " Records."
        self.sendNotification()

    def dailyUpdate(self, lastDateJSON, tableName):
        for entry in lastDateJSON:
            tableName.put_item(Item={
            'Date': entry["Date"],
            'Country_Region': entry["Country_Region"],
            'Recovered': entry["Recovered"],
            'cases': entry["cases"],
            'deaths': entry["deaths"]
        })
        self.notificationMessage = "ETL Job has completed. Updated 1 Record."
        self.sendNotification()

    def sendNotification(self):
        sns = boto3.client('sns')

        response = sns.publish(
        TopicArn = self.snsTopicName,
        Message = self.notificationMessage
    )

                
        
