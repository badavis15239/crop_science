import unittest
from app import app, db
from models import WeatherRecord, WeatherStats

class WeatherApiTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/data'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_weather(self):
        response = self.client.get('/api/weather?page=1&per_page=2')
        self.assertEqual(response.status_code, 200)

    def test_get_weather_stats(self):
        response = self.client.get('/api/weather/stats?page=1&per_page=2')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
