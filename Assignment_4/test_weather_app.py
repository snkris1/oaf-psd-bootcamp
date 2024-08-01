import pytest
from unittest.mock import MagicMock, patch
from weather_app import WeatherService, MockedWeatherService, WeatherHandler

# Test WeatherService with caching
def test_weather_service():
    with patch('requests.get') as mock_get:
        # Setup mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'latitude': 37.7749,
            'longitude': -122.4194,
            'generationtime_ms': 0.033974647521972656,
            'utc_offset_seconds': -25200,
            'timezone': 'America/Los_Angeles',
            'timezone_abbreviation': 'PDT',
            'elevation': 18.0,
            'daily_units': {'time': 'iso8601', 'temperature_2m_max': '°C'},
            'daily': {
                'time': ['2024-08-01', '2024-08-02', '2024-08-03', '2024-08-04', '2024-08-05', '2024-08-06', '2024-08-07'],
                'temperature_2m_max': [22.4, 21.7, 22.0, 20.4, 21.6, 23.2, 21.7]
            }
        }
        mock_response.from_cache = False  # Simulate cache miss
        mock_get.return_value = mock_response

        weather_service = WeatherService()
        weather_handler = WeatherHandler(weather_service)
        
        weather_data = weather_handler.get_weather(37.7749, -122.4194, 'temperature_2m_max', 'America/Los_Angeles')
        
        assert weather_data['latitude'] == 37.7749
        assert weather_data['daily']['temperature_2m_max'] == [22.4, 21.7, 22.0, 20.4, 21.6, 23.2, 21.7]
        mock_get.assert_called_once()

# Test MockedWeatherService
def test_mocked_weather_service():
    weather_service = MockedWeatherService()
    weather_handler = WeatherHandler(weather_service)
    
    weather_data = weather_handler.get_weather(38.0, -122.0, 'temperature_2m_max', 'America/Los_Angeles')
    
    assert weather_data['latitude'] == 37.993515
    assert weather_data['daily']['temperature_2m_max'] == [33.1, 33.7, 35.8, 32.8, 34.3, 37.1, 36.1]

# Test WeatherHandler error handling
def test_weather_handler_error():
    weather_service = MagicMock()
    weather_service.fetch_weather_data.side_effect = Exception('API Error')
    weather_handler = WeatherHandler(weather_service)
    
    result = weather_handler.get_weather(37.7749, -122.4194, 'temperature_2m_max', 'America/Los_Angeles')
    
    assert result == "An error occurred: API Error"

# Run the tests
if __name__ == "__main__":
    pytest.main()