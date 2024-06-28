import json
from unittest import TestCase
from unittest.mock import Mock, patch
from app_lambda.app.case.get_cases import handler, _get_cases_by_injury_type

class TestGetCasesByInjuryType(TestCase):

    @patch("app_lambda.app.case.get_cases._get_cases_by_injury_type")
    def test_get_cases_handler(self, mock_get_cases_by_injury_type):
        injury_type = "Broken Bone"
        request_payload = {"body": {"injuryType": injury_type}}
        mock_get_cases_by_injury_type.return_value = _get_mock_data()

        response = handler(request_payload, "")

        assert response["statusCode"] == 200
        assert "body" in response
        assert len(response["body"]) == 1


    @patch("app_lambda.app.db_config.DbConfig.get_table")
    def test_get_cases_by_injury_type(self, mock_get_table):
        injury_type = "Broken Bone"

        mock_query = Mock()
        mock_get_table.return_value.query  = mock_query 

        mock_query.return_value = _get_mock_data_response()

        response = _get_cases_by_injury_type(injury_type)

        assert len(response) == 1
        self.assertEqual(response[0]["injuryType"], injury_type)


def _get_mock_data():
    return [
        {
            "caseId": "123",
            "injuryType": "Broken Bone",
            "createdDateTime": "2024-06-17T14:46:28.387134",
            "patientId": 12345,
            "description": "Twisted ankle while playing basketball",
            "injuryDate": "2024-06-15",
            "physiotherapistId": 98765,
        }
    ]

def _get_mock_data_response():
    return {
        "Items": _get_mock_data()
    }