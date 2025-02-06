import unittest
from app import app, db, WeatherRecord, WeatherStats

class WeatherApiTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup database configuration before tests"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@0.0.0.0/data'  # Replace with your DB URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # We don't need to call db.init_app(app) again since it's already done in app.py
    
    def setUp(self):
        """Setup the test client for each test"""
        # Create a new app instance for testing
        with app.app_context():  # Use application context
            db.create_all()  # Ensure the tables are created for testing

        # Initialize the test client
        self.client = app.test_client()

    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables after each test to keep the tests isolated

    def test_weather(self):
        response = self.client.get('/api/weather?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('data', data)
        self.assertIn('page', data)
        self.assertIn('per_page', data)
        self.assertIn('total', data)

    def test_weather_stats(self):
        response = self.client.get('/api/weather/stats?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('data', data)
        self.assertIn('page', data)
        self.assertIn('per_page', data)
        self.assertIn('total', data)

if __name__ == '__main__':
    unittest.main()
