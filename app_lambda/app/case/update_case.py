from app_lambda.app.db_config import DbConfig
from botocore.exceptions import ClientError


def handler(event, _):

    update_data = event.get("body")

    try:
        response = update_case(update_data)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            error_response = {
                "Error": {
                    "Code": "Invalid DB Update",
                    "Message": "Request Failed",
                },
                "ResponseMetadata": {"HTTPStatusCode": 400},
            }
            operation_name = "UpdateItem"
            raise ClientError(
                operation_name=operation_name, error_response=error_response
            )
    except ClientError as error:
        print(f"Error updating case {update_data['caseId']}: {error}")

        return {"statusCode": 500, "body": "Case updated failed"}

    return {"statusCode": 200, "body": "Case updated successfully"}


def update_case(update_data):
    return DbConfig.get_table(table_name="Cases").update_item(
        Key={"InjuryType": update_data["injuryType"], "CaseId": update_data["caseId"]},
        UpdateExpression="SET PatientId = :p, Description = :d, InjuryDate = :d, PhysiotherapistId = :i",
        ExpressionAttributeValues={
            ":p": update_data["patientId"],
            ":d": update_data["description"],
            ":i": update_data["physiotherapistId"],
        },
        ReturnValues="UPDATED_NEW",
    )
