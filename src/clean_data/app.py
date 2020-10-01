import json, sys, os, boto3

sys.path.append("transformation/")
import transform_data as transform

usURL = os.environ['US_DATA']
hopkinsURL = os.environ['JH_DATA']
dynamoDBTableName = os.environ['TABLE_NAME']
snsTopicName = os.environ['TOPIC_NAME']

def main(event, context):
    transform_data()

def transform_data():
    transform.Main(usURL, hopkinsURL, dynamoDBTableName, snsTopicName).readData()
