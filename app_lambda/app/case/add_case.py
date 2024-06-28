import json
from datetime import datetime
from app_lambda.app.db_config import DbConfig
from app_lambda.app.id_function import generate_uuid
import pytz
import logging
from botocore.exceptions import ClientError


def handler(event, _):

    body = event.get("body", "{}")

    try:
        new_record = _convert_db_format(body)
        
        case_table = DbConfig.get_table(table_name="Cases")
        response = case_table.put_item(Item=new_record)
        
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            error_response = {
                "Error": {
                    "Code": "Invalid Case Create",
                    "Message": "Request Failed",
                },
                "ResponseMetadata": {"HTTPStatusCode": 500},
            }
            operation_name = "CreateItem"
            raise ClientError(
                operation_name=operation_name, error_response=error_response
            )

        response_payload= {
           "case_id": new_record["CaseId"] 
        }

        return {
            "statusCode": 200,
            "body": response_payload
        }
    except:
        logging.exception("Error while creating case")
        
        return {
            "statusCode": 500,
            "body": "Case creation failed"
        }


def _convert_db_format(body):
    return {
        "InjuryType": body["injuryType"],
        "CaseId": generate_uuid(),
        "CreatedDatetime": datetime.now(pytz.timezone('Asia/Singapore')).isoformat(),
        "PatientId": body["patientId"],
        "Description": body["description"],
        "InjuryDate": body["injuryDate"],
        "PhysiotherapistId": body["physiotherapistId"],
    }
