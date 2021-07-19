from fastapi.testclient import TestClient
from app import app
from unittest.mock import patch

client = TestClient(app)

def test_generate_chart():
    response = client.get('chart_link')
    assert response.status_code == 201
    assert isinstance(response.json().get('chart_url'), str)

def test_get_chart_not_ready():
    response = client.get('chart')
    assert response.status_code == 404
    response = client.get('chart/not_id_of_ready_task')
    assert response.status_code == 202

@patch('app.AsyncResult', autospec=True)
def test_get_chart_ready(mock_result_class):
    instance = mock_result_class.return_value
    instance.ready.return_value = True
    instance.get.return_value = '<html></html>'
    response = client.get('chart/some_valid_id')
    assert response.status_code == 200