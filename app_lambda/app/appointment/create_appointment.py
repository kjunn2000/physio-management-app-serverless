import json
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:4566")
table = dynamodb.Table("Appointment")

def lambda_handler(event, _):
    body = json.loads(event['body'])
    
    appointment = {
        'AppointmentId': body.get('appointmentId'),
        'AppointmentDate': body.get('appointmentDate'),
        'AppointmentStartTime': body.get('appointmentStartTime'),
        'AppointmentEndTime': body.get('appointmentEndTime'),
        'CaseId': body.get('caseId'),
        'PhysiotherapistId': body.get('physiotherapistId'),
    }
    
    table.put_item(Item=appointment)
    
    # Return a success response
    response = {
        'statusCode': 200,
        'body': json.dumps(f"Appointment record created for case {appointment['CaseId']}")
    }
    
    return response

event = {
    "body": json.dumps({
        "appointmentId": "appt-456",
        "appointmentDate": "2024-06-02",
        "appointmentStartTime": "10:00:00Z",
        "appointmentEndTime": "11:00:00Z",
        "caseId": "case-123",
        "physiotherapistId": "physio-789",
    })
}
lambda_handler(event, None)