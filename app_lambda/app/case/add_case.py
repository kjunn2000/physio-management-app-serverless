import json
from datetime import datetime
from ..db_config import DbConfig
from ..id_function import generate_uuid
import pytz
import logging


def handler(event, _):

    body = json.loads(event)["body"]

    try:
        new_record = _convert_db_format(body)
        
        case_table = DbConfig.get_table("Cases")
        case_table.put_item(Item=new_record)

        resopnse_payload = {
           "case_id": new_record["CaseId"] 
        }
    except:
        logging.exception("Error while creating case")

    return {
        "statusCode": 200,
        "body": resopnse_payload
    }


def _convert_db_format(body):

    return {
        "InjuryType": body["injury_type"],
        "CaseId": generate_uuid(),
        "CreatedDatetime": datetime.now(pytz.timezone('Asia/Singapore')),
        "PatientId": body["patient_id"],
        "Description": body["description"],
        "InjuryDate": body["injury_date"],
        "PhysiotherapistId": body["physiotherapist_id"],
    }

if __name__ == "__main__":
    event = {
        "body" : {
          "injury_type": "Ankle Sprain",
          "patient_id": 12345,
          "description": "Twisted ankle while playing basketball",
          "injury_date": "2024-06-15",
          "physiotherapist_id": 98765
        }
    }
    
    event = json.dumps(event)

    handler(event, "")
