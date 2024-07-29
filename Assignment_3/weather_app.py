class WeatherApplication:
    def __init__(self):
        self.weather_service = WeatherService()
    
    def get_weather(self, city_name: str):
        data = self.weather_service.fetch_weather_data(city_name)
        if data:
            weather_data = WeatherData(data['temperature'], data['humidity'])
            return weather_data
        else:
            return None

class WeatherService:
    def fetch_weather_data(self, city_name: str):
        pass

class WeatherData:
    def __init__(self, temperature: float, humidity: float):
        self.temperature = temperature
        self.humidity = humidity
    
    def __str__(self):
        return f"Temperature: {self.temperature}°C, Humidity: {self.humidity}%"

class City:
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return self.name
