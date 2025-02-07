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


# import os
# import unittest
# from app import app, db, WeatherRecord, WeatherStats

# USERNAME = os.getenv('ADMIN_USER')
# PASSWORD = os.getenv('ADMIN_PASSWORD')
# HOST = os.getenv('HOST')
# DATABASE = os.getenv('DATABASE')
# PORT = os.getenv('PORT')

# class WeatherApiTests(unittest.TestCase):
    
#     @classmethod
#     def setUpClass(cls):
#         """Setup database configuration before tests"""
#         app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}'  # Replace with your DB URI
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#         # We don't need to call db.init_app(app) again since it's already done in app.py
    
#     def setUp(self):
#         """Setup the test client for each test"""
#         # Create a new app instance for testing
#         with app.app_context():  # Use application context
#             db.create_all()  # Ensure the tables are created for testing

#         # Initialize the test client
#         self.client = app.test_client()

#     def tearDown(self):
#         """Clean up after each test"""
#         with app.app_context():
#             db.session.remove()
#             db.drop_all()  # Drop all tables after each test to keep the tests isolated

#     def test_weather(self):
#         response = self.client.get('/api/weather?page=1&per_page=10')
#         self.assertEqual(response.status_code, 200)
#         data = response.get_json()
#         self.assertIn('data', data)
#         self.assertIn('page', data)
#         self.assertIn('per_page', data)
#         self.assertIn('total', data)

#     def test_weather_stats(self):
#         response = self.client.get('/api/weather/stats?page=1&per_page=10')
#         self.assertEqual(response.status_code, 200)
#         data = response.get_json()
#         self.assertIn('data', data)
#         self.assertIn('page', data)
#         self.assertIn('per_page', data)
#         self.assertIn('total', data)

# if __name__ == '__main__':
#     unittest.main()
