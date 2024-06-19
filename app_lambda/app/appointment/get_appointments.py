import json
import boto3

def lambda_handler(event, context):
    body = json.loads(event['body'])
    appointment_date = body.get('appointmentDate')
    dynamodb = boto3.client('dynamodb', endpoint_url="http://127.0.0.1:4566")
    table_name = 'Appointment'
    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression="#ad = :date",
        ExpressionAttributeNames={"#ad": "AppointmentDate"},
        ExpressionAttributeValues={":date": {"S": appointment_date}}
    )
    appointments = response.get('Items', [])
    
    return {
        'statusCode': 200,
        'body': json.dumps(appointments)
    }

event = {
    "body": "{\"appointmentDate\": \"2024-06-02\"}"
}
lambda_handler(event, None)