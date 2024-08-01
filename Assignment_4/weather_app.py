import requests
import requests_cache

requests_cache.install_cache('weather_cache', expire_after=3600)
    
class WeatherService:
    def fetch_weather_data(self, latitude: float, longitude: float, daily_weather_variable: str, timezone: str):
        base_url = "https://api.open-meteo.com/v1/forecast"
        params = {}
        params['latitude'] = latitude
        params['longitude'] = longitude
        params['daily'] = daily_weather_variable
        params['timezone'] = timezone

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            if response.from_cache:
                print("Response served from cache")
            else:
                print("Response served from API")
            return response.json()
        else:
            response.raise_for_status()

class MockedWeatherService:
    def fetch_weather_data(self, latitude: float, longitude: float, daily_weather_variable: str, timezone: str):
        # hardcoded response but I would imagine each time a call is made to the API the response could be saved to 
        # a dictionary with a unique key composed from the params dictionary. Is this the right idea?
        return {
            'latitude': 37.993515, 'longitude': -121.996826, 'generationtime_ms': 0.033020973205566406, 
            'utc_offset_seconds': -25200, 'timezone': 'America/Los_Angeles', 'timezone_abbreviation': 
            'PDT', 'elevation': 31.0, 'daily_units': {'time': 'iso8601', 'temperature_2m_max': '°C'}, 
            'daily': {'time': ['2024-08-01', '2024-08-02', '2024-08-03', '2024-08-04', '2024-08-05', 
            '2024-08-06', '2024-08-07'], 'temperature_2m_max': [33.1, 33.7, 35.8, 32.8, 34.3, 37.1, 36.1]}
        }
    
class WeatherHandler:
    def __init__(self, weatherservice_in):
        self.weatherservice = weatherservice_in

    def get_weather(self, latitude: float, longitude: float, daily_weather_variable: str, timezone: str):
        try:
            daily_data = self.weatherservice.fetch_weather_data(latitude, longitude, daily_weather_variable, timezone)
            if daily_data:
                return daily_data
            else:
                return "Weather data not available"
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == "__main__":
    weather_service = WeatherService()
    latitude = 38.0
    longitude = -122.0
    daily_weather_variable = 'temperature_2m_max'
    timezone = 'America/Los_Angeles'

    weather_handler = WeatherHandler(weather_service)

    weather_data = weather_handler.get_weather(latitude, longitude, daily_weather_variable, timezone)
    print(f"API Weather Service: {weather_data}")

    print("-------------------------------------------------")

    weather_service = MockedWeatherService()
    weather_handler = WeatherHandler(weather_service)
    weather_data = weather_handler.get_weather(latitude, longitude, daily_weather_variable, timezone)
    print(f"Mocked Weather Service: {weather_data}")

