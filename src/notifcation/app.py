from __future__ import print_function
import json, sys, os, boto3

snsTopicName = os.environ['TOPIC_NAME']
sns = boto3.client('sns')

def main(event, context):
    jsonResponse = {'status': False, 'TotalItems': {}, 'Items': []}
    message = "No data has been processed"

    if not 'Records' in event:
        jsonResponse = {'status': False, "error_message" : 'No Records found in Event' }
        return jsonResponse

    for r in event.get('Records'):
        if r.get('eventName') == "INSERT":
            d = {}
            d['Date'] = r['dynamodb']['NewImage']['Date']['S']
            if 'Message' in r['dynamodb']['NewImage']:
                d['Message'] = r['dynamodb']['NewImage']['Message']['S']
            jsonResponse['Items'].append(d)

    if jsonResponse.get('Items'):
        jsonResponse['status'] = True
        jsonResponse['TotalItems'] = { 'Received': len( event.get('Records') ) , 'Processed': len( jsonResponse.get('Items') ) }
        processed = jsonResponse["TotalItems"]["Processed"]
        received = jsonResponse["TotalItems"]["Received"]
        
        message = "Data has been inserted. Total Items [ Processed: " + str(processed) +  " Received: " + str(received) + " ]"
    
    print(jsonResponse)
    
    print(message)

    response = sns.publish(
        TopicArn = snsTopicName,
        Message = message
    )
