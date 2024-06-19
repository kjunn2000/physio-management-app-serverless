import json
import os
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:4566")
table = dynamodb.Table("patient")

def handler(event, context):
    # Parse the request body
    body = json.loads(event['body'])
    
    # Define the patient record
    patient = {
        'patient_id': body['patient_id'],
        'name': body['name'],
        'age': body['age'],
        'gender': body['gender'],
        'contact': body['contact']
    }
    
    # Put the patient record in DynamoDB
    table.put_item(Item=patient)
    # Return a success response
    response = {
        'statusCode': 200,
        'body': json.dumps(f"Patient record created for {patient['name']}")
    }
    
    return response