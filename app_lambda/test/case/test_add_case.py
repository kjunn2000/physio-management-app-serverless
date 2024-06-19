import json
from unittest import TestCase
from unittest.mock import Mock, patch
from ...app.case.add_case import handler, _convert_db_format


class TestAddCase(TestCase):

    @patch(
        "app_lambda.app.case.add_case._convert_db_format",
        return_value={
            "InjuryType": "Ankle Sprain",
            "CaseId": "123e4567-e89b-12d3-a456-426614174000",
        },
    )
    @patch("app_lambda.app.db_config.DbConfig.get_table")
    def test_add_case_handler(self, mock_get_table, _):
        event = {
            "body": {
                "injury_type": "Ankle Sprain2",
                "patient_id": 12345,
                "description": "Twisted ankle while playing basketball",
                "injury_date": "2024-06-15",
                "physiotherapist_id": 98765,
            }
        }

        mock_put_item = Mock()
        mock_get_table.return_value.put_item = mock_put_item

        response = handler(json.dumps(event), "")

        assert response["statusCode"] == 200

    def test_convert_db_format(self):
        test_data = {
            "injury_type": "Ankle Sprain",
            "patient_id": "XXXX",
            "description": "Twisted ankle while playing basketball",
            "injury_date": "2024-06-15",
            "physiotherapist_id": "XXXXX",
        }

        result = _convert_db_format(test_data)

        assert result["InjuryType"] == "Ankle Sprain"
        assert "CaseId" in result
