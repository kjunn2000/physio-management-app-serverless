from ..app.run import call
from unittest.mock import patch

@patch("app_lambda.app.run.mock_input", return_value = 3)
def test_import(mock_run):
    value = call()
    assert value == 3