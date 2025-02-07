import os
import unittest
import requests

# Load environment variables
API_BASE_URL = os.getenv('API_BASE_URL', 'http://0.0.0.0:5000')  # Default to local if not set

class WeatherApiTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Prints the base URL to debug connection issues."""
        print(f"Testing API at: {API_BASE_URL}")

    def test_weather(self):
        """Test fetching paginated weather data."""
        url = f"{API_BASE_URL}/api/weather?page=1&per_page=10"
        response = requests.get(url)

        self.assertEqual(response.status_code, 200, f"Unexpected response: {response.text}")
        data = response.json()

        self.assertIn('data', data)
        self.assertIn('page', data)
        self.assertIn('per_page', data)
        self.assertIn('total', data)

    def test_weather_stats(self):
        """Test fetching paginated weather statistics."""
        url = f"{API_BASE_URL}/api/weather/stats?page=1&per_page=10"
        response = requests.get(url)

        self.assertEqual(response.status_code, 200, f"Unexpected response: {response.text}")
        data = response.json()

        self.assertIn('data', data)
        self.assertIn('page', data)
        self.assertIn('per_page', data)
        self.assertIn('total', data)

if __name__ == '__main__':
    unittest.main()

