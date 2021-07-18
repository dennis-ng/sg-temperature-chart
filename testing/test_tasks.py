import unittest
from unittest.mock import patch
from tasks import get_weather
from datetime import date, timedelta

class Test_Tasks(unittest.TestCase):

    @patch('models.temperature.plot')
    @patch('models.temperature.get_day_weather')
    @patch('models.temperature.date')
    def test_get_weather(self, mock_date, mock_get_day_weather, mock_plot):
        mock_today = date(2021, 7, 7)
        mock_date.today.return_value = mock_today
        expected_called_dates = (mock_today - timedelta(days=i) for i in reversed(range(7)))

        get_weather()
        mock_get_day_weather.has_calls(expected_called_dates, any_order=True)
        assert mock_get_day_weather.call_count == 7
        mock_plot.assert_called_once()


    def test_get_weather_schema(self):
        chart = get_weather() # ValidationError if API schema changed
        assert chart.startswith('<html>')
        assert chart.endswith('</html>')
