import json
from unittest import TestCase
from unittest.mock import Mock, patch
from app_lambda.app.case.add_case import handler, _convert_db_format


class TestAddCase:

    def test_add_case_handler(self, mocker):
        mock_return_value_convert_db_format = {
            "InjuryType": "Ankle Sprain",
            "CaseId": "123e4567-e89b-12d3-a456-426614174000",
        }
        mocker.patch("app_lambda.app.case.add_case._convert_db_format", return_value = mock_return_value_convert_db_format)
        
        mock_get_table = mocker.patch( "app_lambda.app.db_config.DbConfig.get_table")
        mock_add_item_response = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        mock_get_table.return_value.put_item.return_value = mock_add_item_response

        event = {
            "body": {
                "injuryType": "Ankle Sprain2",
                "patientId": 12345,
                "description": "Twisted ankle while playing basketball",
                "injuryDate": "2024-06-15",
                "physiotherapistId": 98765,
            }
        }

        response = handler(event, "")

        assert response["statusCode"] == 200

    def test_convert_db_format(self):
        test_data = {
            "injuryType": "Ankle Sprain",
            "patientId": "XXXX",
            "description": "Twisted ankle while playing basketball",
            "injuryDate": "2024-06-15",
            "physiotherapistId": "XXXXX",
        }

        result = _convert_db_format(test_data)

        assert result["InjuryType"] == "Ankle Sprain"
        assert "CaseId" in result
