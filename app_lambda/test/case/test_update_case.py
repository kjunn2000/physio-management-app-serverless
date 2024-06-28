from app_lambda.app.case.update_case import handler, update_case
from botocore.exceptions import ClientError
import pytest

event = {
    "body": {
        "caseId": 1,
        "injuryType": "Ankle Sprain2",
        "patientId": 12345,
        "description": "Twisted ankle while playing basketball",
        "injuryDate": "2024-06-15",
        "physiotherapistId": 98765,
    }
}


class TestUpdateCase:

    def test_update_handler(self, mocker):
        mock_update_item_response = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        mocker.patch(
            "app_lambda.app.case.update_case.update_case",
            return_value=mock_update_item_response,
        )

        response = handler(event, None)

        assert response is not None
        assert response["statusCode"] == 200
        assert response["body"] == "Case updated successfully"

    def test_handler_client_error(self, mocker):

        error_response = {
            "Error": {
                "Code": "ThrottlingException",
                "Message": "Request throttled",
            },
            "ResponseMetadata": {"HTTPStatusCode": 500},
        }
        operation_name = "UpdateItem"

        client_error = ClientError(
            operation_name=operation_name, error_response=error_response
        )

        mocker.patch(
            "app_lambda.app.case.update_case.update_case", side_effect=client_error
        )

        response = handler(event, None)

        assert response is not None
        assert response["statusCode"] == 500
        assert response["body"] == "Case updated failed"

    def test_update_case(self, mocker):
        mock_get_table = mocker.patch( "app_lambda.app.db_config.DbConfig.get_table")
        mock_update_item_response = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        mock_get_table.return_value.update_item.return_value = mock_update_item_response

        response = update_case(event["body"])

        assert response is not None
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    def test_update_client_error(self, mocker):

        error_response = {
            "Error": {
                "Code": "ThrottlingException",
                "Message": "Request throttled",
            },
            "ResponseMetadata": {"HTTPStatusCode": 500},
        }
        operation_name = "UpdateItem"

        mock_get_table = mocker.patch("app_lambda.app.db_config.DbConfig.get_table")

        mock_get_table.return_value.update_item.side_effect = ClientError(
            operation_name=operation_name, error_response=error_response
        )
        
        with pytest.raises(ClientError):
            update_case(event["body"])
